import boto3

ec2 = boto3.client("ec2", endpoint_url="http://localhost:4566")
resp = ec2.run_instances(ImageId="ami-123456", MinCount=1, MaxCount=1, InstanceType="t2.micro")
print("EC2 instance simulated:", resp["Instances"])
