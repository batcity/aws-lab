import boto3

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566")
table = dynamodb.create_table(
    TableName="Users",
    KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
    AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
    BillingMode="PAY_PER_REQUEST"
)
table.wait_until_exists()
table.put_item(Item={"id": "1", "name": "Alice"})
print(table.get_item(Key={"id": "1"})["Item"])
