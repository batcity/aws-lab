# EC2 Example

This example demonstrates how to **simulate AWS EC2 (Elastic Compute Cloud) instances locally** using **LocalStack** and **Boto3**.

---

## What is EC2?

Amazon EC2 is a **web service that provides resizable compute capacity in the cloud**.  

> ⚠️ “Resizable” does **not** mean you can dynamically increase CPU or memory of a running instance. It means you can **choose or change instance types** to adjust compute resources, and you can scale the number of instances up or down as needed.

It allows you to run **virtual servers**—think of them like cloud-based VMs—without managing physical hardware.

### Key Concepts

- **Instance**: A virtual server in AWS EC2. Acts like a remote computer you can control programmatically.
- **AMI (Amazon Machine Image)**: A template with an operating system and optional software used to launch an instance.
- **Instance Type**: Defines CPU, memory, storage, and networking capacity. Example: `t2.micro`, `m5.large`.
- **Regions & Availability Zones (AZs)**: Instances run in a specific region/AZ for high availability.
- **Elastic IP**: A static public IP that can be assigned to instances.
- **Security Groups**: Virtual firewalls controlling inbound/outbound traffic.
- **Key Pairs**: Used for SSH access to Linux instances.

### Use Cases

- Web servers and backend APIs
- Batch processing or data pipelines
- Development and testing environments
- Hosting containerized applications

---

## What This Example Does

The `ec2.py` script demonstrates a **basic EC2 workflow** using LocalStack:

```python
import boto3

ec2 = boto3.client("ec2", endpoint_url="http://localhost:4566")
resp = ec2.run_instances(
    ImageId="ami-123456",
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro"
)
print("EC2 instance simulated:", resp["Instances"])
````

### Step-by-Step

1. **Connect to EC2 locally**
   Uses `boto3.client("ec2")` with LocalStack’s endpoint (`http://localhost:4566`) instead of AWS.
2. **Launch an instance**
   Runs one instance (`MinCount=1, MaxCount=1`) using a dummy AMI (`ami-123456`) and type `t2.micro`.
3. **Inspect the response**
   Prints the simulated instance metadata, like instance ID, state, and type.

> ⚠️ This is a **simulation using LocalStack**. No real AWS resources are created, so there are no charges.

---

## Intermediate AWS Dev Notes

* **Lifecycle**: EC2 instances go through `pending → running → stopping → stopped → terminated`.
* **Pricing**: Instances are billed per second (or hour) while running. Spot and Reserved instances reduce cost.
* **Networking**: Instances reside in a VPC, with subnets, security groups, and route tables.
* **AMIs**: Choosing the right AMI affects startup time, OS, and pre-installed software.
* **Instance Metadata**: Applications can query instance metadata (like ID, region, etc.).
* **Scaling**: Auto Scaling groups dynamically scale EC2 instances based on demand.
* **Integration**: EC2 integrates with other AWS services like S3, RDS, Lambda, CloudWatch, and IAM.

---

## How to Run

1. Make sure **LocalStack** is running:

```bash
localstack start
```

2. Run the EC2 script:

```bash
python ec2/ec2.py
```

3. You should see a simulated EC2 instance printed in the console.

---

## References

* [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/index.html)
* [Boto3 EC2 Client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html)
* [LocalStack EC2 Support](https://docs.localstack.cloud/references/aws/ec2/)
