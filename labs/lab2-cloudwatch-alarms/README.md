# Lab 2: Automated Alerting (CloudWatch Alarms & SNS)

**Goal:** Now that we have a custom metric tracking errors, create a CloudWatch Alarm that triggers an SNS email notification if the error count reaches our threshold.

```bash
# 1. Create an SNS Topic for Alerts
TOPIC_ARN=$(awslocal sns create-topic --name CriticalAlertsTopic --query 'TopicArn' --output text)
TOPIC_ARN=$(aws sns create-topic --name CriticalAlertsTopic --query 'TopicArn' --output text)

# 2. Subscribe an email address to the Topic
awslocal sns subscribe \
  --topic-arn $TOPIC_ARN \
  --protocol email \
  --notification-endpoint admin@mycompany.com
aws sns subscribe \
  --topic-arn $TOPIC_ARN \
  --protocol email \
  --notification-endpoint admin@mycompany.com

# 3. Create a CloudWatch Alarm tied to the Metric Filter from Lab 1
awslocal cloudwatch put-metric-alarm \
  --alarm-name "HighErrorRateAlarm" \
  --metric-name AppErrorCount \
  --namespace MyApp \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --alarm-actions $TOPIC_ARN
aws cloudwatch put-metric-alarm \
  --alarm-name "HighErrorRateAlarm" \
  --metric-name AppErrorCount \
  --namespace MyApp \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --alarm-actions $TOPIC_ARN

# 4. Manually publish custom metric data to simulate a sudden spike and trigger the alarm
awslocal cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name AppErrorCount \
  --value 5 \
  --unit Count
aws cloudwatch put-metric-data \
  --namespace MyApp \
  --metric-name AppErrorCount \
  --value 5 \
  --unit Count
```

## 🧠 Key Concepts & Importance

- **CloudWatch Alarms:** Watch a single metric over a time period that you specify, and perform one or more actions based on the value of the metric relative to a given threshold over a number of time periods.
- **Amazon SNS (Simple Notification Service):** A fully managed messaging service for both system-to-system and person-to-person communication.
- **SNS Topic:** A logical access point and communication channel that groups together endpoints (such as email, SMS, or Lambda).
- **Alarm States:**
    - `OK`: The metric is within the defined threshold.
    - `ALARM`: The metric is outside the defined threshold.
    - `INSUFFICIENT_DATA`: The alarm has just started, the metric is not available, or not enough data is available for the metric to determine the alarm state.
- **Thresholds & Evaluation:** You define the condition (e.g., `GreaterThanOrEqualToThreshold`) and the number of periods the condition must be met to trigger the alarm.

## 🛠️ Command Reference

- `sns create-topic`: Creates a topic to which messages can be published.
    - `--name`: The name of the topic.
- `sns subscribe`: Prepares to subscribe an endpoint by sending the endpoint a confirmation message.
    - `--topic-arn`: The ARN of the topic you want to subscribe to.
    - `--protocol`: The protocol you want to use (e.g., `email`, `sms`, `lambda`, `sqs`).
    - `--notification-endpoint`: The endpoint that you want to receive notifications (e.g., an email address).
- `cloudwatch put-metric-alarm`: Creates or updates an alarm and associates it with a metric.
    - `--alarm-name`: The name for the alarm.
    - `--metric-name`: The name for the metric associated with the alarm.
    - `--namespace`: The namespace for the metric.
    - `--statistic`: The statistic for the metric (e.g., `Sum`, `Average`).
    - `--period`: The length, in seconds, used to evaluate the metric.
    - `--evaluation-periods`: The number of periods over which data is compared to the specified threshold.
    - `--threshold`: The value against which the specified statistic is compared.
    - `--comparison-operator`: The arithmetic operation to use when comparing the specified statistic and threshold.
    - `--alarm-actions`: The actions to execute when this alarm transitions to an ALARM state from any other state.
- `cloudwatch put-metric-data`: Publishes metric data points to Amazon CloudWatch.
    - `--namespace`: The namespace for the metric data.
    - `--metric-name`: The name of the metric.
    - `--value`: The value for the metric.
    - `--unit`: The unit for the metric (e.g., `Count`, `Percent`).

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
