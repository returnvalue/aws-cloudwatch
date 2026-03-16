import boto3
import time

logs = boto3.client('logs', endpoint_url="http://localhost:4566", region_name="us-east-1")

logs.create_log_group(logGroupName='/app/production')
logs.create_log_stream(logGroupName='/app/production', logStreamName='instance-01')

logs.put_metric_filter(
    logGroupName='/app/production',
    filterName='ErrorCountFilter',
    filterPattern='ERROR',
    metricTransformations=[{
        'metricName': 'AppErrorCount',
        'metricNamespace': 'MyApp',
        'metricValue': '1'
    }]
)

timestamp = int(time.time() * 1000)
logs.put_log_events(
    logGroupName='/app/production',
    logStreamName='instance-01',
    logEvents=[
        {'timestamp': timestamp, 'message': '[INFO] Service started successfully.'},
        {'timestamp': timestamp, 'message': '[ERROR] Database connection failed.'}
    ]
)
