# Infrastructure Management (Terraform) 🏗️

This directory contains the Infrastructure as Code (IaC) configuration for the Smart Citizen Reporter. It uses **Terraform** to provision and manage the complete AWS environment in the `ap-south-1` (Mumbai) region.

## 🌟 Managed Resources

- **VPC & Networking**: Custom VPC, 2 Public Subnets, Internet Gateway, and Route Tables.
- **EC2 Instance**: `t2.micro` running Ubuntu 24.04 with Docker pre-installed via User Data.
- **RDS (PostgreSQL)**: `db.t3.micro` managed database instance.
- **S3 Bucket**: Publicly accessible bucket for storing user-submitted issue images.
- **SNS Topic**: `smart-citizen-alerts` for real-time notification of critical issues.
- **IAM Roles**: 
  - `ec2_role`: Allows the application to upload to S3 and publish to SNS.
  - `lambda_role`: Execution role for background image processing.
- **Lambda Function**: Placeholder function triggered for image handling.

## 🚀 How to Use

### Prerequisites
1. [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli).
2. Configure your AWS CLI credentials.

### Provisioning
To create or update the infrastructure, run from this directory:

```bash
# Initialize Terraform
terraform init

# Preview the changes
terraform plan

# Apply the configuration
terraform apply -auto-approve
```

### Outputs
After a successful `apply`, Terraform will provide:
- `ec2_ip`: The public IP of your web server.
- `rds_endpoint`: The connection string for the database.
- `s3_bucket`: The unique name of your upload bucket.
- `sns_topic_arn`: The ARN needed for critical alerts.

## 📁 File Structure

- `provider.tf`: AWS provider and region settings.
- `vpc.tf`: Core networking infrastructure.
- `ec2.tf`: Instance configuration, Security Groups, and IAM.
- `rds.tf`: PostgreSQL database settings.
- `s3_sns.tf`: Storage and notification configurations.
- `lambda.tf`: Serverless processing resources.
- `user_data.sh`: Bash script that automates the application launch on the EC2.

## ⚠️ Important Notes
- **Security**: Database passwords and GitHub tokens are injected via environment variables or variables file for production security.
- **Cost**: The configuration is optimized for the **AWS Free Tier**.
