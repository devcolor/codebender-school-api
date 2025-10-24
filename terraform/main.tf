# Configure the AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2" # Oregon region
}

# ECR Repository
resource "aws_ecr_repository" "devcolor00_school" {
  name                 = "devcolor00-school"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name        = "devcolor00-school"
    Environment = "production"
    Project     = "devcolor-backend"
  }
}

# ECR Repository Policy
resource "aws_ecr_repository_policy" "devcolor00_school_policy" {
  repository = aws_ecr_repository.devcolor00_school.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowPushPull"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload"
        ]
      }
    ]
  })
}

# Get current AWS account ID
data "aws_caller_identity" "current" {}

# IAM Role for App Runner
resource "aws_iam_role" "apprunner_instance_role" {
  name = "devcolor00-school-apprunner-instance-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name    = "devcolor00-school-apprunner-instance-role"
    Project = "devcolor-backend"
  }
}

# IAM Role for App Runner Access
resource "aws_iam_role" "apprunner_access_role" {
  name = "devcolor00-school-apprunner-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name    = "devcolor00-school-apprunner-access-role"
    Project = "devcolor-backend"
  }
}

# Attach ECR access policy to App Runner access role
resource "aws_iam_role_policy_attachment" "apprunner_access_ecr" {
  role       = aws_iam_role.apprunner_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# App Runner Service
resource "aws_apprunner_service" "devcolor00_school" {
  service_name = "devcolor00-school"

  source_configuration {
    image_repository {
      image_configuration {
        port = "8000"
        runtime_environment_variables = {
          DB_HOST     = var.db_host
          DB_USER     = var.db_user
          DB_PASSWORD = var.db_password
          DB_PORT     = var.db_port
        }
      }
      image_identifier      = "${aws_ecr_repository.devcolor00_school.repository_url}:latest"
      image_repository_type = "ECR"
    }
    access_role_arn = aws_iam_role.apprunner_access_role.arn
  }

  instance_configuration {
    cpu    = "0.25 vCPU"
    memory = "0.5 GB"
  }

  health_check_configuration {
    healthy_threshold   = 1
    interval            = 10
    path                = "/"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 5
  }

  tags = {
    Name        = "devcolor00-school"
    Environment = "production"
    Project     = "devcolor-backend"
  }

  depends_on = [
    aws_iam_role_policy_attachment.apprunner_access_ecr
  ]
}
