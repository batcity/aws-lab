import boto3

apigateway = boto3.client("apigateway", endpoint_url="http://localhost:4566")
rest_api = apigateway.create_rest_api(name="MyAPI")
print("API created:", rest_api["id"])
