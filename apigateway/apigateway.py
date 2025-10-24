import boto3

apigateway = boto3.client("apigateway", endpoint_url="http://localhost:4566")
rest_api = apigateway.create_rest_api(name="MyAPI")
print("API created:", rest_api["id"])
print("API retrieval example:")
print(apigateway.get_rest_api(restApiId=rest_api["id"]))


print("Listing all APIs:")
for api in apigateway.get_rest_apis()["items"]:
    print(api["name"], api["id"])
    
print("deleting all APIs:")
for api in apigateway.get_rest_apis()["items"]:
    apigateway.delete_rest_api(restApiId=api["id"])
print("All APIs deleted.")
