import boto3

sns = boto3.client('sns', endpoint_url="http://localhost:4566", region_name="us-east-1")
cloudwatch = boto3.client('cloudwatch', endpoint_url="http://localhost:4566", region_name="us-east-1")

topic_response = sns.create_topic(Name='CriticalAlertsTopic')
topic_arn = topic_response['TopicArn']

sns.subscribe(
    TopicArn=topic_arn,
    Protocol='email',
    Endpoint='admin@mycompany.com'
)

cloudwatch.put_metric_alarm(
    AlarmName='HighErrorRateAlarm',
    MetricName='AppErrorCount',
    Namespace='MyApp',
    Statistic='Sum',
    Period=300,
    EvaluationPeriods=1,
    Threshold=1.0,
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    AlarmActions=[topic_arn]
)

cloudwatch.put_metric_data(
    Namespace='MyApp',
    MetricData=[{
        'MetricName': 'AppErrorCount',
        'Value': 5.0,
        'Unit': 'Count'
    }]
)
