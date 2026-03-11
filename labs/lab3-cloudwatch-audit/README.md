# Lab 3: API Auditing with AWS CloudTrail

**Goal:** Security and compliance require tracking who did what and when. We will create a multi-region CloudTrail to log all AWS API calls into a secure S3 bucket.

```bash
# 1. Create the destination S3 bucket for the audit logs
awslocal s3api create-bucket --bucket organization-audit-logs

# 2. Add a bucket policy allowing CloudTrail to write to it
cat <<EOF > trail-bucket-policy.json
{
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
EOF
awslocal s3api put-bucket-policy --bucket organization-audit-logs --policy file://trail-bucket-policy.json

# 3. Create and Start the multi-region CloudTrail
awslocal cloudtrail create-trail \
  --name GlobalAuditTrail \
  --s3-bucket-name organization-audit-logs \
  --is-multi-region-trail

awslocal cloudtrail start-logging --name GlobalAuditTrail
```

## 🧠 Key Concepts & Importance

- **AWS CloudTrail:** A service that enables governance, compliance, operational auditing, and risk auditing of your AWS account. It records API calls made by or on behalf of an AWS account.
- **Audit Logs:** CloudTrail provides a history of AWS API calls for your account, including API calls made through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.
- **Multi-Region Trail:** A trail that is applied to all regions. This ensures that you are logging activity in every region of your AWS account, even those you aren't actively using.
- **S3 Bucket Policy for CloudTrail:** CloudTrail requires specific permissions to write log files to your S3 bucket. The policy must allow CloudTrail to check the bucket ACL and put objects into the specified path.
- **Governance & Compliance:** CloudTrail is foundational for security and compliance, providing the "who, what, where, and when" for every action in your infrastructure.

## 🛠️ Command Reference

- `s3api create-bucket`: Creates a new S3 bucket.
- `s3api put-bucket-policy`: Replaces the policy on a bucket.
    - `--bucket`: The name of the bucket.
    - `--policy`: The JSON policy document.
- `cloudtrail create-trail`: Creates a trail that specifies the settings for delivery of log data to an S3 bucket.
    - `--name`: The name of the trail.
    - `--s3-bucket-name`: The name of the S3 bucket designated for publishing log files.
    - `--is-multi-region-trail`: Specifies whether the trail is created in the current region or in all regions.
- `cloudtrail start-logging`: Starts the recording of AWS API calls and delivery of log files for the specified trail.
    - `--name`: The name of the trail to start logging for.
