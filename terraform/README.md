# Terraform Infrastructure for DevColor Backend

This Terraform configuration sets up AWS infrastructure for the DevColor Backend application using ECR and App Runner in the Oregon (us-west-2) region.

## Resources Created

- **ECR Repository**: `devcolor00-school` for storing Docker images
- **App Runner Service**: `devcolor00-school` for running the application
- **IAM Roles**: Required roles for App Runner to access ECR

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform installed** (version 1.0+)
3. **Database accessible** from AWS (for environment variables)

## Setup Instructions

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 1.5. Fix IAM Permissions (If Using Existing User)

If you're using an existing IAM user like `devcolor-school`, you need to attach the proper policy:

**Option A: Using AWS CLI**
```bash
# Create the policy
aws iam create-policy \
  --policy-name devcolor-school-github-actions-policy \
  --policy-document file://iam-policy-only.json

# Attach to existing user
aws iam attach-user-policy \
  --user-name devcolor-school \
  --policy-arn arn:aws:iam::509399615930:policy/devcolor-school-github-actions-policy
```

**Option B: Using AWS Console**
1. Go to IAM → Users → devcolor-school
2. Click "Add permissions" → "Attach policies directly"
3. Create new policy using the JSON from `iam-policy-only.json`
4. Attach the policy to the user

### 2. Configure Variables

Copy the example variables file and update with your values:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your database configuration:

```hcl
db_host     = "your-database-host"
db_user     = "your-database-user"
db_password = "your-database-password"
db_port     = "3306"
aws_region  = "us-west-2"
```

### 3. Plan and Apply

```bash
# Review the planned changes
terraform plan

# Apply the infrastructure
terraform apply
```

### 4. Configure GitHub Secrets

After applying Terraform, add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `APPRUNNER_SERVICE_ARN`: The App Runner service ARN (from Terraform output)

Get the App Runner service ARN:
```bash
terraform output apprunner_service_arn
```

## Outputs

- `ecr_repository_url`: ECR repository URL for pushing images
- `apprunner_service_url`: Public URL of your deployed application
- `apprunner_service_arn`: ARN for the App Runner service (needed for GitHub Actions)

## GitHub Actions Integration

The GitHub Actions workflow will:

1. **Build** the Docker image from `docker/Dockerfile`
2. **Push** to ECR with both commit SHA and `latest` tags
3. **Deploy** to App Runner (only on main branch pushes)

## App Runner Configuration

- **CPU**: 0.25 vCPU
- **Memory**: 0.5 GB
- **Port**: 8000
- **Health Check**: HTTP on `/` endpoint
- **Auto Scaling**: Managed by AWS App Runner

## Cost Considerations

- **ECR**: Pay for storage of Docker images
- **App Runner**: Pay for vCPU and memory usage
- **Minimal cost** for small applications (~$5-10/month)

## Cleanup

To destroy all resources:

```bash
terraform destroy
```

## Troubleshooting

### Common Issues

1. **ECR Permission Denied**: Ensure AWS credentials have ECR permissions
2. **App Runner Deployment Failed**: Check application logs in AWS Console
3. **Database Connection**: Verify database is accessible from AWS

### Useful Commands

```bash
# Check ECR repository
aws ecr describe-repositories --repository-names devcolor00-school --region us-west-2

# Check App Runner service
aws apprunner describe-service --service-arn $(terraform output -raw apprunner_service_arn)

# View App Runner logs
aws logs describe-log-groups --log-group-name-prefix "/aws/apprunner/devcolor00-school"
```
