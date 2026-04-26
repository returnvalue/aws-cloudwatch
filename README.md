# AWS CloudWatch Monitoring Labs (LocalStack Pro)

![AWS](https://img.shields.io/badge/AWS-CloudWatch_Monitoring-FF9900?style=for-the-badge&logo=amazonaws)
![LocalStack](https://img.shields.io/badge/LocalStack-Pro-000000?style=for-the-badge)

This repository contains hands-on labs demonstrating core Amazon CloudWatch concepts, from log management and metric filtering to automated alarms and dashboards. Using [LocalStack Pro](https://localstack.cloud/), we simulate a complete AWS monitoring environment locally.

## 🎯 Architecture Goals & Use Cases Covered
Based on AWS best practices (SAA-C03), these labs cover:
* **Log Management:** Creating log groups and streams to centralize application logs.
* **Metric Filters:** Automatically extracting numerical data from text logs for monitoring.
* **CloudWatch Alarms:** Setting thresholds to trigger notifications or automated actions via SNS.
* **Custom Metrics:** Publishing application-specific data points for monitoring.
* **API Auditing:** Implementing CloudTrail to track account activity for security and compliance.
* **Continuous Compliance:** Using AWS Config to automate resource evaluation and reporting.
* **Secure Operations:** Managing secrets and configuration with SSM Parameter Store.

## ⚙️ Prerequisites

* [Docker](https://docs.docker.com/get-docker/) & Docker Compose
* [LocalStack Pro](https://app.localstack.cloud/) account and Auth Token
* [`awslocal` CLI](https://github.com/localstack/awscli-local) (a wrapper around the AWS CLI for LocalStack)

## 🚀 Environment Setup

1. Configure your LocalStack Auth Token in `.env`:
   ```bash
   echo "YOUR_TOKEN=your_auth_token_here" > .env
   ```

2. Start LocalStack Pro:
   ```bash
   docker-compose up -d
   ```

> [!IMPORTANT]
> **Cumulative Architecture:** These labs are designed as a cumulative scenario. You are building an evolving monitoring infrastructure.

## 📚 Labs Index
1. [Lab 1: CloudWatch Logs & Metric Filters](./labs/lab1-cloudwatch-logs/README.md)
2. [Lab 2: Automated Alerting (CloudWatch Alarms & SNS)](./labs/lab2-cloudwatch-alarms/README.md)
3. [Lab 3: API Auditing with AWS CloudTrail](./labs/lab3-cloudwatch-audit/README.md)
4. [Lab 4: Continuous Compliance (AWS Config)](./labs/lab4-cloudwatch-config/README.md)
5. [Lab 5: Secure Operations (Systems Manager Parameter Store)](./labs/lab5-cloudwatch-ssm/README.md)

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
