resource "aws_ssm_parameter" "db_password" {
  name        = "/production/database/password"
  description = "Production RDS Password"
  type        = "SecureString"
  value       = "SuperSecretDBPassword123!"
}
