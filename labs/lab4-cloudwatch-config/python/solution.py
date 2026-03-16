import boto3
import json

iam = boto3.client('iam', endpoint_url="http://localhost:4566", region_name="us-east-1")
config = boto3.client('config', endpoint_url="http://localhost:4566", region_name="us-east-1")
s3api = boto3.client('s3', endpoint_url="http://localhost:4566", region_name="us-east-1")

trust_policy = {
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "config.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}

with open('config-trust.json', 'w') as f:
    json.dump(trust_policy, f)

role_response = iam.create_role(
    RoleName='AWSConfigRole',
    AssumeRolePolicyDocument=json.dumps(trust_policy)
)
role_arn = role_response['Role']['Arn']

config.put_configuration_recorder(
    ConfigurationRecorder={
        'name': 'default',
        'roleARN': role_arn,
        'recordingGroup': {
            'allSupported': True,
            'includeGlobalResourceTypes': True
        }
    }
)

s3api.create_bucket(Bucket='config-delivery-bucket')

config.put_delivery_channel(
    DeliveryChannel={
        'name': 'default',
        's3BucketName': 'config-delivery-bucket'
    }
)

config.start_configuration_recorder(ConfigurationRecorderName='default')

config_rule = {
  "ConfigRuleName": "s3-bucket-versioning-enabled",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_VERSIONING_ENABLED"
  }
}

with open('config-rule.json', 'w') as f:
    json.dump(config_rule, f)

config.put_config_rule(ConfigRule=config_rule)
