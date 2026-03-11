# Lab 4: Continuous Compliance (AWS Config)

**Goal:** Instead of manually checking if resources meet security standards, use AWS Config to continuously evaluate infrastructure. We will deploy a rule ensuring all S3 buckets have versioning enabled.

```bash
# 1. Create an IAM Role allowing AWS Config to scan resources
cat <<EOF > config-trust.json
{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "config.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}
EOF
CONFIG_ROLE_ARN=$(awslocal iam create-role --role-name AWSConfigRole --assume-role-policy-document file://config-trust.json --query 'Role.Arn' --output text)

# 2. Create the Configuration Recorder
awslocal configservice put-configuration-recorder \
  --configuration-recorder name=default,roleARN=$CONFIG_ROLE_ARN \
  --recording-group allSupported=true,includeGlobalResourceTypes=true

# 3. Create an S3 Bucket to act as the Delivery Channel destination
awslocal s3api create-bucket --bucket config-delivery-bucket

# 4. Attach the Delivery Channel to AWS Config
awslocal configservice put-delivery-channel \
  --delivery-channel name=default,s3BucketName=config-delivery-bucket

# 5. NOW we can successfully start the Configuration Recorder
awslocal configservice start-configuration-recorder --configuration-recorder-name default

# 6. Deploy an AWS Managed Rule to check for S3 Bucket Versioning
cat <<EOF > config-rule.json
{
  "ConfigRuleName": "s3-bucket-versioning-enabled",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"
  }
}
EOF
awslocal configservice put-config-rule --config-rule file://config-rule.json
```

## 🧠 Key Concepts & Importance

- **AWS Config:** A service that enables you to assess, audit, and evaluate the configurations of your AWS resources.
- **Continuous Monitoring:** AWS Config continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations.
- **Configuration Recorder:** Stores the configuration of the supported resources in your account as configuration items (CIs).
- **Delivery Channel:** Defines where AWS Config delivers configuration snapshots and configuration history files (e.g., an S3 bucket).
- **Config Rules:** Represent your ideal configuration settings. AWS Config provides managed rules for common security and compliance standards, or you can create custom rules.
- **Compliance Status:** Rules evaluate your resources as they are created or modified. You can see at a glance which resources are compliant and which are not.

## 🛠️ Command Reference

- `iam create-role`: Creates a service role for AWS Config.
- `configservice put-configuration-recorder`: Records configuration changes for supported resource types.
    - `--configuration-recorder`: Specifies the name and role for the recorder.
    - `--recording-group`: Specifies which resource types to record.
- `s3api create-bucket`: Creates the bucket used for the delivery channel.
- `configservice put-delivery-channel`: Configures where AWS Config sends configuration data.
    - `--delivery-channel`: Specifies the name and destination bucket.
- `configservice start-configuration-recorder`: Activates the recording of resource configurations.
- `configservice put-config-rule`: Deploys a compliance rule to evaluate resources.
    - `--config-rule`: The JSON definition of the rule (e.g., `S3_BUCKET_VERSIONING_ENABLED`).
