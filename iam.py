import boto3
import json

# Role and instance profile names
role_name = "iam_role"
instance_profile_name = "instance_profile"

# Assume role policy
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ec2.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}

# S3 permissions policy ARN
policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"

# Initialize the IAM client
iam_client = boto3.client('iam')

# Create the IAM Role
iam_client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(assume_role_policy)
)
print(f"IAM Role {role_name} created.")

# Attach S3 permissions to the role
iam_client.attach_role_policy(
    RoleName=role_name,
    PolicyArn=policy_arn
)
print(f"S3 permissions attached to IAM Role {role_name}.")

# Create the instance profile
iam_client.create_instance_profile(
    InstanceProfileName=instance_profile_name
)
print(f"Instance profile {instance_profile_name} created.")

# Get the ARN of the IAM role
role_response = iam_client.get_role(RoleName=role_name)
role_arn = role_response['Role']['Arn']

# Add the role to the instance profile
iam_client.add_role_to_instance_profile(
    InstanceProfileName=instance_profile_name,
    RoleName=role_name
)
print(f"IAM role {role_name} added to instance profile {instance_profile_name}.")
