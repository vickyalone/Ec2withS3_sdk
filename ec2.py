import os
import boto3

# Replace these values with your specific details
bucket_name = 'buckettprefix-3'
iam_role_arn = 'arn:aws:iam::497595539056:role/iam_role'
instance_profile_arn = 'arn:aws:iam::497595539056:instance-profile/instance_profile'
region_name = 'ap-south-1'  # Specify the AWS region, e.g., 'us-east-1'

# Set your AWS credentials as environment variables
# Function to launch EC2 instance
def launch_ec2_instance(image_id, instance_type, key_name, security_group_ids, subnet_id, iam_role_arn, user_data_script):
    ec2 = boto3.resource('ec2', region_name=region_name)

    # You can remove the create_key_pair function since you're using an existing key pair

    instance = ec2.create_instances(
        ImageId=image_id,
        InstanceType=instance_type,
        KeyName=key_name,  # Use the existing key pair name
        SecurityGroupIds=security_group_ids,
        SubnetId=subnet_id,
        IamInstanceProfile={
            'Arn': instance_profile_arn
        },
        UserData=user_data_script,
        MinCount=1,
        MaxCount=1
    )[0]

    instance.wait_until_running()
    instance.load()

    return instance

# Main function
def main():
    # Replace these values with your specific details
    image_id = 'ami-090e20427fcf22649'  # Specify the correct Ubuntu 22 LTS AMI ID
    instance_type = 't4g.micro'
    key_name = 'vicky'  # Specify the existing key pair name

    # User data script to upload a text file to S3 bucket
    user_data_script = """#!/bin/bash

# Install Python
sudo apt-get update
sudo apt-get install -y python3

# Install AWS CLI
sudo apt-get install -y awscli

# Create an informational file
echo "Private IP Address: $(curl http://169.254.169.254/latest/meta-data/local-ipv4)" > /tmp/ec2_info.txt
echo "Hostname: $(hostname)" >> /tmp/ec2_info.txt

# Copy the file to S3 bucket
aws s3 cp /tmp/ec2_info.txt s3://buckettprefix-3/  

"""

    # Launch EC2 instance
    instance = launch_ec2_instance(image_id, instance_type, key_name, [], '', instance_profile_arn, user_data_script)

    print(f"EC2 Instance ID: {instance.id}")

if __name__ == "__main__":
    main()
