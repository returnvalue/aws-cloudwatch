resource "aws_cloudwatch_log_group" "app_production" {
  name = "/app/production"
}

resource "aws_cloudwatch_log_stream" "instance_01" {
  name           = "instance-01"
  log_group_name = aws_cloudwatch_log_group.app_production.name
}

resource "aws_cloudwatch_log_metric_filter" "error_count" {
  name           = "ErrorCountFilter"
  pattern        = "ERROR"
  log_group_name = aws_cloudwatch_log_group.app_production.name

  metric_transformation {
    name      = "AppErrorCount"
    namespace = "MyApp"
    value     = "1"
  }
}
