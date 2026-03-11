resource "aws_iam_role" "config_role" {
  name = "AWSConfigRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "config.amazonaws.com" }
    }]
  })
}

resource "aws_config_configuration_recorder" "main" {
  name     = "default"
  role_arn = aws_iam_role.config_role.arn
}

resource "aws_s3_bucket" "config_bucket" {
  bucket = "config-delivery-bucket"
}

resource "aws_config_delivery_channel" "main" {
  name           = "default"
  s3_bucket_name = aws_s3_bucket.config_bucket.id
}

resource "aws_config_config_rule" "s3_versioning" {
  name = "s3-bucket-versioning-enabled"
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }
}
