import boto3
from botocore.exceptions import ClientError

# FAKE credentials - DO NOT use real credentials like this!
AWS_ACCESS_KEY = 'AKIA9876FAKE5432DEMO'
AWS_SECRET_KEY = 'jk2390FAKE8461demo5789DUMMY9032keys'
AWS_REGION = 'us-west-2'

def create_s3_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region using provided credentials"""
    
    try:
        # Create S3 client with credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=region if region else 'us-east-1'
        )

        # Create the bucket
        if region is None or region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )

        print(f"Creating bucket '{bucket_name}'...")
        
        # Wait until the bucket is created
        s3_client.get_waiter('bucket_exists').wait(Bucket=bucket_name)
        
        print("Bucket created successfully!")
        
        # Add default bucket policy (private)
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        
        return True

    except ClientError as e:
        print(f"An error occurred: {e}")
        return False

def main():
    # Example usage
    bucket_name = "my-test-bucket-20250626"  # Remember bucket names must be globally unique
    region = "us-west-2"
    
    if create_s3_bucket(bucket_name, region):
        print(f"Bucket '{bucket_name}' is ready to use in region '{region}'")
    else:
        print("Bucket creation failed")

if __name__ == "__main__":
    main()





