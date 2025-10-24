# IAM User for GitHub Actions
resource "aws_iam_user" "github_actions" {
  name = "devcolor-school-github-actions"
  path = "/"

  tags = {
    Name    = "devcolor-school-github-actions"
    Project = "devcolor-backend"
    Purpose = "GitHub Actions CI/CD"
  }
}

# IAM Policy for ECR and App Runner access
resource "aws_iam_policy" "github_actions_policy" {
  name        = "devcolor-school-github-actions-policy"
  description = "Policy for GitHub Actions to access ECR and App Runner"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
        Resource = aws_ecr_repository.devcolor00_school.arn
      },
      {
        Effect = "Allow"
        Action = [
          "apprunner:StartDeployment",
          "apprunner:DescribeService"
        ]
        Resource = aws_apprunner_service.devcolor00_school.arn
      }
    ]
  })
}

# Attach policy to user
resource "aws_iam_user_policy_attachment" "github_actions_policy_attachment" {
  user       = aws_iam_user.github_actions.name
  policy_arn = aws_iam_policy.github_actions_policy.arn
}

# Access keys for GitHub Actions (create manually for security)
resource "aws_iam_access_key" "github_actions" {
  user = aws_iam_user.github_actions.name
}

# Output the access key (will be shown in terraform output)
output "github_actions_access_key_id" {
  description = "Access Key ID for GitHub Actions"
  value       = aws_iam_access_key.github_actions.id
}

output "github_actions_secret_access_key" {
  description = "Secret Access Key for GitHub Actions"
  value       = aws_iam_access_key.github_actions.secret
  sensitive   = true
}
