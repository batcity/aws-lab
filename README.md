# AWS Lab (LocalStack Edition)

Learn the most commonly used AWS services locally using LocalStack and Boto3 without an AWS account.

## Table of Contents

### Storage
- [S3](./s3/README.md)

### Compute
- [EC2](./ec2/README.md)
- [Lambda](./lambda/README.md)

### Databases
- [DynamoDB](./dynamodb/README.md)

### API & Serverless
- [API Gateway](./apigateway/README.md)

### ETL / Data Processing
- [Glue / PySpark ETL](./glue_etl/README.md)

## Setup

1. Run:
    ```bash
    . ./setup.sh
    ```
2. Start LocalStack:
    ```bash
    localstack start
    ```
3. Run Python scripts, e.g.:
    ```bash
    python s3/s3_example.py
    python lambda/hello_lambda.py
    ```
