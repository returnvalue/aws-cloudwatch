# Lab 5: Secure Operations (Systems Manager Parameter Store)

**Goal:** Stop embedding database passwords in your application code. Store them securely in SSM Parameter Store using KMS encryption, and retrieve them programmatically.
```bash
# 1. Store a secure, encrypted parameter (Simulating a DB password)
# Note: Using single quotes prevents bash from misinterpreting special characters like '!'
awslocal ssm put-parameter \
  --name '/production/database/password' \
  --value 'SuperSecretDBPassword123!' \
  --type 'SecureString' \
  --description 'Production RDS Password'
aws ssm put-parameter \
  --name '/production/database/password' \
  --value 'SuperSecretDBPassword123!' \
  --type 'SecureString' \
  --description 'Production RDS Password'

# 2. Programmatically retrieve and decrypt the parameter
awslocal ssm get-parameter \
  --name '/production/database/password' \
  --with-decryption \
  --query 'Parameter.Value' \
  --output text
aws ssm get-parameter \
  --name '/production/database/password' \
  --with-decryption \
  --query 'Parameter.Value' \
  --output text
```

## 🧠 Key Concepts & Importance

- **AWS Systems Manager Parameter Store:** Provides secure, hierarchical storage for configuration data management and secrets management.
- **SecureString:** A parameter type that uses AWS Key Management Service (KMS) to encrypt the parameter value. This is ideal for sensitive data like passwords, license keys, or database connection strings.
- **Decoupling Configuration:** Storing configuration and secrets separately from your code allows you to change values without redeploying your application.
- **Access Control:** You can use IAM policies to control which users and services have access to specific parameters, following the principle of least privilege.
- **Auditability:** Parameter Store logs all access and changes, providing a clear audit trail for sensitive configuration data.

## 🛠️ Command Reference

- `ssm put-parameter`: Creates or updates a parameter in the Parameter Store.
    - `--name`: The hierarchical name of the parameter (e.g., `/production/database/password`).
    - `--value`: The data you want to store.
    - `--type`: The type of parameter (e.g., `String`, `StringList`, or `SecureString`).
    - `--description`: A brief description of the parameter.
- `ssm get-parameter`: Retrieves the value of a single parameter.
    - `--name`: The name of the parameter to retrieve.
    - `--with-decryption`: Set to true to return the decrypted value of a `SecureString` parameter.
    - `--query`: Filters the output to return only the parameter value.
    - `--output`: Sets the output format (e.g., `text`).

---

💡 **Pro Tip: Using `aws` instead of `awslocal`**

If you prefer using the standard `aws` CLI without the `awslocal` wrapper or repeating the `--endpoint-url` flag, you can configure a dedicated profile in your AWS config files.

### 1. Configure your Profile
Add the following to your `~/.aws/config` file:
```ini
[profile localstack]
region = us-east-1
output = json
# This line redirects all commands for this profile to LocalStack
endpoint_url = http://localhost:4566
```

Add matching dummy credentials to your `~/.aws/credentials` file:
```ini
[localstack]
aws_access_key_id = test
aws_secret_access_key = test
```

### 2. Use it in your Terminal
You can now run commands in two ways:

**Option A: Pass the profile flag**
```bash
aws iam create-user --user-name DevUser --profile localstack
```

**Option B: Set an environment variable (Recommended)**
Set your profile once in your session, and all subsequent `aws` commands will automatically target LocalStack:
```bash
export AWS_PROFILE=localstack
aws iam create-user --user-name DevUser
```

### Why this works
- **Precedence**: The AWS CLI (v2) supports a global `endpoint_url` setting within a profile. When this is set, the CLI automatically redirects all API calls for that profile to your local container instead of the real AWS cloud.
- **Convenience**: This allows you to use the standard documentation commands exactly as written, which is helpful if you are copy-pasting examples from AWS labs or tutorials.
