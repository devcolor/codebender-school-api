#!/bin/bash

# Terraform deployment script for DevColor Backend

echo "🚀 Starting Terraform deployment for DevColor Backend..."

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo "❌ terraform.tfvars not found!"
    echo "📝 Please copy terraform.tfvars.example to terraform.tfvars and update with your values:"
    echo "   cp terraform.tfvars.example terraform.tfvars"
    echo "   # Then edit terraform.tfvars with your database details"
    exit 1
fi

# Initialize Terraform
echo "🔧 Initializing Terraform..."
terraform init

if [ $? -ne 0 ]; then
    echo "❌ Terraform init failed!"
    exit 1
fi

# Validate configuration
echo "✅ Validating Terraform configuration..."
terraform validate

if [ $? -ne 0 ]; then
    echo "❌ Terraform validation failed!"
    exit 1
fi

# Plan deployment
echo "📋 Planning Terraform deployment..."
terraform plan -out=tfplan

if [ $? -ne 0 ]; then
    echo "❌ Terraform plan failed!"
    exit 1
fi

# Ask for confirmation
echo ""
echo "🤔 Do you want to apply this plan? (y/N)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "🚀 Applying Terraform configuration..."
    terraform apply tfplan
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Deployment completed successfully!"
        echo ""
        echo "📊 Important outputs:"
        echo "ECR Repository URL:"
        terraform output ecr_repository_url
        echo ""
        echo "App Runner Service URL:"
        terraform output apprunner_service_url
        echo ""
        echo "App Runner Service ARN (for GitHub secrets):"
        terraform output apprunner_service_arn
        echo ""
        echo "🔑 Next steps:"
        echo "1. Add the App Runner Service ARN to your GitHub secrets as 'APPRUNNER_SERVICE_ARN'"
        echo "2. Push to main branch to trigger deployment"
    else
        echo "❌ Terraform apply failed!"
        exit 1
    fi
else
    echo "❌ Deployment cancelled by user"
    rm -f tfplan
    exit 0
fi
