output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.devcolor00_school.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN"
  value       = aws_ecr_repository.devcolor00_school.arn
}

output "apprunner_service_url" {
  description = "App Runner service URL"
  value       = aws_apprunner_service.devcolor00_school.service_url
}

output "apprunner_service_arn" {
  description = "App Runner service ARN"
  value       = aws_apprunner_service.devcolor00_school.arn
}

output "apprunner_service_id" {
  description = "App Runner service ID"
  value       = aws_apprunner_service.devcolor00_school.service_id
}
