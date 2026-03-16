import boto3

ssm = boto3.client('ssm', endpoint_url="http://localhost:4566", region_name="us-east-1")

ssm.put_parameter(
    Name='/production/database/password',
    Value='SuperSecretDBPassword123!',
    Type='SecureString',
    Description='Production RDS Password'
)

response = ssm.get_parameter(
    Name='/production/database/password',
    WithDecryption=True
)

print(response['Parameter']['Value'])
