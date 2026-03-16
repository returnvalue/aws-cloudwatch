import boto3
import json

s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")
cloudtrail = boto3.client('cloudtrail', endpoint_url="http://localhost:4566", region_name="us-east-1")

s3api.create_bucket(Bucket='organization-audit-logs')

bucket_policy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::organization-audit-logs"
    },
    {
      "Effect": "Allow",
      "Principal": {"Service": "cloudtrail.amazonaws.com"},
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::organization-audit-logs/AWSLogs/*",
      "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
    }
  ]
}

with open('trail-bucket-policy.json', 'w') as f:
    json.dump(bucket_policy, f)

s3api.put_bucket_policy(
    Bucket='organization-audit-logs',
    Policy=json.dumps(bucket_policy)
)

cloudtrail.create_trail(
    Name='GlobalAuditTrail',
    S3BucketName='organization-audit-logs',
    IsMultiRegionTrail=True
)

cloudtrail.start_logging(Name='GlobalAuditTrail')
