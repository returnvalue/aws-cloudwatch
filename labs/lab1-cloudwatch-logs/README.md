# Lab 1: CloudWatch Logs & Metric Filters

**Goal:** Applications generate logs continuously. Instead of manually searching for errors, we will create a Metric Filter that automatically scans incoming CloudWatch logs for the word "ERROR" and converts it into a numerical metric.

```bash
# 1. Create a Log Group and a Log Stream
awslocal logs create-log-group --log-group-name /app/production
aws logs create-log-group --log-group-name /app/production
awslocal logs create-log-stream --log-group-name /app/production --log-stream-name instance-01
aws logs create-log-stream --log-group-name /app/production --log-stream-name instance-01

# 2. Create a Metric Filter to count "ERROR" occurrences
awslocal logs put-metric-filter \
  --log-group-name /app/production \
  --filter-name ErrorCountFilter \
  --filter-pattern "ERROR" \
  --metric-transformations metricName=AppErrorCount,metricNamespace=MyApp,metricValue=1
aws logs put-metric-filter \
  --log-group-name /app/production \
  --filter-name ErrorCountFilter \
  --filter-pattern "ERROR" \
  --metric-transformations metricName=AppErrorCount,metricNamespace=MyApp,metricValue=1

# 3. Simulate an application writing logs using inline dynamic timestamps
awslocal logs put-log-events \
  --log-group-name /app/production \
  --log-stream-name instance-01 \
  --log-events "[{\"timestamp\": $(date +%s000), \"message\": \"[INFO] Service started successfully.\"}, {\"timestamp\": $(date +%s000), \"message\": \"[ERROR] Database connection failed.\"}]"
aws logs put-log-events \
  --log-group-name /app/production \
  --log-stream-name instance-01 \
  --log-events "[{\"timestamp\": $(date +%s000), \"message\": \"[INFO] Service started successfully.\"}, {\"timestamp\": $(date +%s000), \"message\": \"[ERROR] Database connection failed.\"}]"
```

## 🧠 Key Concepts & Importance

- **Log Groups:** A group of log streams that share the same retention, monitoring, and access control settings.
- **Log Streams:** A sequence of log events that share the same source (e.g., a specific EC2 instance or Lambda function).
- **Metric Filters:** Define patterns to search for in log data as it's sent to CloudWatch Logs. CloudWatch Logs uses these patterns to turn log data into numerical CloudWatch metrics.
- **Metric Namespace:** A container for CloudWatch metrics. Metrics in different namespaces are isolated from each other.
- **Log Events:** A record of some activity recorded by the application or resource being monitored. Each event contains a timestamp and a raw data message.

## 🛠️ Command Reference

- `logs create-log-group`: Creates a new log group.
    - `--log-group-name`: The name of the log group.
- `logs create-log-stream`: Creates a new log stream within a log group.
    - `--log-group-name`: The name of the log group.
    - `--log-stream-name`: The name of the log stream.
- `logs put-metric-filter`: Creates or updates a metric filter and associates it with the specified log group.
    - `--log-group-name`: The name of the log group.
    - `--filter-name`: A name for the metric filter.
    - `--filter-pattern`: A symbolic description of how CloudWatch Logs should interpret the data in each log event.
    - `--metric-transformations`: Describes how to transform log data into a CloudWatch metric.
- `logs put-log-events`: Uploads a batch of log events to the specified log stream.
    - `--log-group-name`: The name of the log group.
    - `--log-stream-name`: The name of the log stream.
    - `--log-events`: The log events, including timestamp and message.

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
