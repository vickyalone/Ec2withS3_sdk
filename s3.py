import boto3

# Replace 'your-region' with your desired AWS region
region = 'ap-south-1'

# Create S3 buckets
prefix = "buckettprefix-"
for i in range(1, 6):
    bucket_name = f"{prefix}{i}"
    s3_client = boto3.client('s3', region_name=region)
    s3_client.create_bucket(Bucket=bucket_name)
    print(f"S3 bucket {bucket_name} created.")
