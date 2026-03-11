resource "aws_s3_bucket" "audit_logs" {
  bucket = "organization-audit-logs"
}

resource "aws_s3_bucket_policy" "cloudtrail_policy" {
  bucket = aws_s3_bucket.audit_logs.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "s3:GetBucketAcl"
        Effect   = "Allow"
        Principal = { Service = "cloudtrail.amazonaws.com" }
        Resource = aws_s3_bucket.audit_logs.arn
      },
      {
        Action   = "s3:PutObject"
        Effect   = "Allow"
        Principal = { Service = "cloudtrail.amazonaws.com" }
        Resource = "${aws_s3_bucket.audit_logs.arn}/AWSLogs/*"
        Condition = {
          StringEquals = { "s3:x-amz-acl" = "bucket-owner-full-control" }
        }
      }
    ]
  })
}

resource "aws_cloudtrail" "global" {
  name                          = "GlobalAuditTrail"
  s3_bucket_name                = aws_s3_bucket.audit_logs.id
  is_multi_region_trail         = true
  include_global_service_events = true
  enable_logging                = true
  depends_on                    = [aws_s3_bucket_policy.cloudtrail_policy]
}
