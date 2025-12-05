#!/usr/bin/env python3
"""
apigw_single_script.py

Starts two tiny Flask mock services (service1 on port 5001, service2 on port 5002)
running in background threads (daemon threads). Creates a LocalStack API Gateway
with greedy-proxy resources and demonstrates requests via the gateway,
printing pretty JSON responses so you can see it worked.
"""

import os
import time
import threading
import json
import requests
from flask import Flask, request, jsonify
import boto3

# CONFIG
LOCALSTACK_URL = os.getenv("LOCALSTACK_URL", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

# The hostname where the mock services are reachable *from the LocalStack container*.
# On macOS / Windows, host.docker.internal will work. On Linux you may need BACKEND_HOST=localhost
BACKEND_HOST = os.getenv("BACKEND_HOST", "host.docker.internal")

SERVICE1_PORT = int(os.getenv("SERVICE1_PORT", "5001"))
SERVICE2_PORT = int(os.getenv("SERVICE2_PORT", "5002"))

# Flask mock services (with custom GET responses)
def run_service(port, service_name):
    app = Flask(service_name)

    @app.route("/", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    @app.route("/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    def handler(subpath=""):
        # --- Custom GET responses ------------------------------------------------
        # service1 root GET
        if service_name == "service1" and request.method == "GET" and subpath == "":
            return jsonify({
                "service": "service1",
                "status": "ok",
                "message": "Hello from service1 root GET"
            })

        # service1 health endpoint
        if service_name == "service1" and request.method == "GET" and subpath == "health":
            # uptime is a dummy static value here
            return jsonify({
                "service": "service1",
                "status": "healthy",
                "uptime": 12345
            })

        # service2 special path
        if service_name == "service2" and request.method == "GET" and subpath == "foo/bar":
            return jsonify({
                "service": "service2",
                "status": "ok",
                "special": True,
                "path": "/foo/bar",
                "numbers": [1, 2, 3]
            })

        # -------------------------------------------------------------------------

        # Fallback behavior for all other requests (echo)
        try:
            body = request.get_json(silent=True)
        except Exception:
            body = None

        return jsonify({
            "service": service_name,
            "method": request.method,
            "path": "/" + subpath,
            "args": request.args,
            "body": body
        })

    # run as non-blocking server in a thread; use 0.0.0.0 so container can reach host
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

def start_background_services():
    t1 = threading.Thread(target=run_service, args=(SERVICE1_PORT, "service1"), daemon=True)
    t2 = threading.Thread(target=run_service, args=(SERVICE2_PORT, "service2"), daemon=True)
    t1.start()
    t2.start()
    # give them a moment to start
    time.sleep(1)
    return (t1, t2)


# TODO: code this block again yourself
# API Gateway setup
def create_api_and_integrations():
    apigw = boto3.client(
        "apigateway",
        endpoint_url=LOCALSTACK_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    # Create REST API
    resp = apigw.create_rest_api(name="MyLocalAPI")
    api_id = resp["id"]
    print("Created API:", api_id)

    # Find root resource id
    resources = apigw.get_resources(restApiId=api_id)
    root_id = next((r["id"] for r in resources["items"] if r["path"] == "/"), None)
    if root_id is None:
        raise RuntimeError("Root resource not found")

    # Create /service1 and /service2 resources
    r1 = apigw.create_resource(restApiId=api_id, parentId=root_id, pathPart="service1")
    r2 = apigw.create_resource(restApiId=api_id, parentId=root_id, pathPart="service2")
    r1_id, r2_id = r1["id"], r2["id"]
    print("Created resources:", r1_id, r2_id)

    # Integration URIs: point to host reachable by LocalStack container
    svc1_url = f"http://{BACKEND_HOST}:{SERVICE1_PORT}"
    svc2_url = f"http://{BACKEND_HOST}:{SERVICE2_PORT}"

    # Create ANY method + integration for the exact resource root (e.g. /service1)
    for resource_id, svc_url in ((r1_id, svc1_url), (r2_id, svc2_url)):
        apigw.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            authorizationType="NONE"
        )
        apigw.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod="ANY",
            type="HTTP_PROXY",
            integrationHttpMethod="ANY",
            uri=svc_url  # root of the backend service
        )

    # Create a greedy proxy child under each service so subpaths like /service2/foo/bar are accepted
    for resource_id, svc_url in ((r1_id, svc1_url), (r2_id, svc2_url)):
        proxy = apigw.create_resource(
            restApiId=api_id,
            parentId=resource_id,
            pathPart="{proxy+}"
        )
        proxy_id = proxy["id"]
        # ANY method on the proxy resource
        apigw.put_method(
            restApiId=api_id,
            resourceId=proxy_id,
            httpMethod="ANY",
            authorizationType="NONE",
            requestParameters={
                "method.request.path.proxy": True
            }
        )
        # Integration: include the proxy path variable in the backend URI so the original path is forwarded
        apigw.put_integration(
            restApiId=api_id,
            resourceId=proxy_id,
            httpMethod="ANY",
            type="HTTP_PROXY",
            integrationHttpMethod="ANY",
            uri=f"{svc_url}/{{proxy}}",
            requestParameters={
                "integration.request.path.proxy": "method.request.path.proxy"
            }
        )

    # Deploy the API
    stage = "dev"
    apigw.create_deployment(restApiId=api_id, stageName=stage)
    print("Deployed API to stage:", stage)

    # Return api id + stage
    return api_id, stage

def pretty_print_response(resp):
    """Print status and attempt to decode JSON, falling back to raw text."""
    print("status:", resp.status_code)
    content_type = resp.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            parsed = resp.json()
            print(json.dumps(parsed, indent=2))
            return
        except Exception:
            pass
    print(resp.text)

def invoke_examples(api_id, stage):
    # LocalStack REST API invocation pattern:
    base = f"{LOCALSTACK_URL}/restapis/{api_id}/{stage}/_user_request_"
    url1 = base + "/service1/"
    url1_health = base + "/service1/health"
    url2 = base + "/service2/foo/bar?x=1"

    print("Invoking service1 via API Gateway (GET root):", url1)
    r1 = requests.get(url1)
    pretty_print_response(r1)

    print("\nInvoking service1 via API Gateway (GET /health):", url1_health)
    r1h = requests.get(url1_health)
    pretty_print_response(r1h)

    print("\nInvoking service2 via API Gateway (GET subpath + query):", url2)
    r2_get = requests.get(url2)
    pretty_print_response(r2_get)

    print("\nInvoking service2 via API Gateway (POST subpath with JSON body):", url2)
    r2_post = requests.post(url2, json={"hello": "world"})
    pretty_print_response(r2_post)

def cleanup(api_id):
    apigw = boto3.client(
        "apigateway",
        endpoint_url=LOCALSTACK_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )
    try:
        apigw.delete_rest_api(restApiId=api_id)
        print("Deleted API:", api_id)
    except Exception as e:
        print("Cleanup error:", e)

if __name__ == "__main__":
    print("Starting two background Flask mock services on ports", SERVICE1_PORT, SERVICE2_PORT)
    start_background_services()

    print("Using BACKEND_HOST =", BACKEND_HOST)
    print("Ensure LocalStack can reach that host from container (host.docker.internal on macOS/Windows).")

    print("Creating API and integrations in LocalStack at", LOCALSTACK_URL)
    api_id, stage = create_api_and_integrations()

    try:
        # small wait before invoking (give LocalStack a moment to register deployment)
        time.sleep(1.0)
        invoke_examples(api_id, stage)
    finally:
        # clean up API resource
        print("Cleaning up API...")
        cleanup(api_id)

    print("Script complete. Background Flask threads are daemonic and will exit when this process exits.")
