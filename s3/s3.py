import boto3
import json
from datetime import datetime

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

s3.create_bucket(Bucket="my-bucket")
s3.put_object(Bucket="my-bucket", Key="hello.txt", Body="Hello LocalStack S3!")

# Pretty-print the response
print(json.dumps(s3.list_objects(Bucket="my-bucket"), indent=4, default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)))
