# Manual AWS Infrastructure Setup Guide 🛠️

This guide provides step-by-step instructions to manually set up the infrastructure for the **Smart Citizen Reporter** application on AWS, staying within the **Free Tier**.

## 1. VPC & Networking
1.  Navigate to the **VPC Console**.
2.  Click **Create VPC**.
3.  Select **VPC and more**.
4.  **Name Tag**: `smart-citizen-manual-vpc`.
5.  **IPv4 CIDR block**: `10.0.0.0/16`.
6.  **Number of Availability Zones (AZs)**: `1` or `2`.
7.  **Number of Public Subnets**: `2`.
8.  **Number of Private Subnets**: `0`.
9.  **DNS hostnames** & **DNS resolution**: Ensure both are enabled.
10. Click **Create VPC**.

## 2. Security Groups
1.  Go to **Security Groups** under EC2.
2.  **Create Security Group**:
    - **Name**: `smart-citizen-ec2-sg`
    - **Description**: Allow Web and SSH
    - **VPC**: Select the VPC created above.
    - **Inbound Rules**:
        - SSH (22) from `0.0.0.0/0`
        - HTTP (80) from `0.0.0.0/0`
3.  **Create another Security Group**:
    - **Name**: `smart-citizen-rds-sg`
    - **Description**: Allow DB traffic from EC2
    - **VPC**: Select the same VPC.
    - **Inbound Rules**:
        - PostgreSQL (5432) from Security Group `smart-citizen-ec2-sg`.

## 3. S3 Bucket
1.  Navigate to the **S3 Console**.
2.  Click **Create bucket**.
3.  **Bucket Name**: `smart-citizen-uploads-<unique-id>` (e.g., `smart-citizen-uploads-abc123`).
4.  **Region**: Same as your VPC.
5.  **Object Ownership**: ACLs enabled, Bucket owner preferred.
6.  **Block Public Access**: **Uncheck** "Block all public access" (to allow users to view their uploaded issue images).
7.  Click **Create bucket**.

## 4. RDS Database (PostgreSQL)
1.  Navigate to the **RDS Console**.
2.  Click **Create database**.
3.  **Engine**: PostgreSQL.
4.  **Template**: **Free Tier**.
5.  **DB Instance Identifier**: `smart-citizen-db`.
6.  **Master Username**: `postgres`.
7.  **Master Password**: `SecurePass123!` (or your choice).
8.  **VPC**: Select your VPC.
9.  **Public Access**: **Yes** (easier for initial testing).
10. **Security Group**: Select `smart-citizen-rds-sg`.
11. Click **Create Database**.

## 5. EC2 Instance
1.  Navigate to the **EC2 Console**.
2.  Click **Launch Instance**.
3.  **Name**: `smart-citizen-server`.
4.  **AMI**: Ubuntu Server 24.04 LTS (Free Tier Eligible).
5.  **Instance Type**: `t2.micro` or `t3.micro`.
6.  **Key Pair**: Select/Create a new one.
7.  **Network Settings**:
    - **VPC**: Your VPC.
    - **Subnet**: Public Subnet.
    - **Auto-assign Public IP**: Enable.
    - **Security Group**: Select `smart-citizen-ec2-sg`.
8.  Click **Launch Instance**.

## 6. SNS Topic (Alerts)
1.  Navigate to the **SNS Console**.
2.  Click **Create topic**.
3.  **Type**: Standard.
4.  **Name**: `smart-citizen-reporter-alerts`.
5.  Click **Create topic**.

## 7. IAM Role for EC2 (S3 & SNS Access)
1.  Navigate to the **IAM Console**.
2.  Click **Roles** -> **Create role**.
3.  **Trusted entity type**: AWS service.
4.  **Service or use case**: EC2.
5.  **Permissions**:
    - Select `AmazonS3FullAccess` (or create a custom policy for specific bucket).
    - Select `AmazonSNSFullAccess`.
6.  **Role Name**: `smart-citizen-reporter-role`.
7.  Click **Create role**.
8.  Go back to your **EC2 instance** -> **Actions** -> **Security** -> **Modify IAM role**.
9.  Select `smart-citizen-reporter-role` and click **Update IAM role**.

## 8. Docker Deployment on EC2
To run your Dockerized application on the EC2 instance:

1.  **SSH into your EC2**:
    ```bash
    ssh -i your-key.pem ubuntu@your-ec2-ip
    ```
2.  **Install Docker**:
    ```bash
    sudo apt update
    sudo apt install docker.io -y
    sudo usermod -aG docker ubuntu
    # Log out and back in for groups to take effect
    ```
3.  **Build your Image**:
    - You can either build it on EC2 or push it to **Amazon ECR**.
    - To build directly on EC2:
    ```bash
    git clone your-repo-url
    cd SmartCitizenReporter
    docker build -t smart-citizen-reporter .
    ```
4.  **Run the Container**:
    ```bash
    docker run -d \
      -p 80:5000 \
      --name smart-citizen-app \
      -e DATABASE_URL='postgresql://postgres:SecurePass123!@your-rds-endpoint:5432/citizenreporter' \
      -e SECRET_KEY='your-secret-key' \
      smart-citizen-reporter:latest
    ```

## 9. Amazon ECR (Optional - Best Practice)
If you want to manage images properly:
1.  Navigate to **ECR Console** -> **Create repository** named `smart-citizen-reporter`.
2.  Follow the **View push commands** provided by AWS in the ECR console to tag and push your local image to the cloud.

## 11. Docker Compose setup
To run both the application and a local PostgreSQL database using Docker Compose:

1.  **Create `docker-compose.yml`** in the project root:
    ```yaml
    version: '3.8'
    services:
      db:
        image: postgres:16
        container_name: smart-citizen-db
        environment:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: citizenreporter
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data

      web:
        build: .
        container_name: smart-citizen-web
        ports:
          - "5000:5000"
        environment:
          - DATABASE_URL=postgresql://user:password@db:5432/citizenreporter
          - SECRET_KEY=your_secret_key_here
          - FLASK_APP=app.py
        depends_on:
          - db
    volumes:
      postgres_data:
    ```
2.  **Run the application**:
    ```bash
    docker compose up -d
    ```

## 12. Database Connection File
The database schema and models are defined in `models.py`. The application uses the `DATABASE_URL` environment variable to connect.
- **Local SQLite**: `sqlite:///instance/site.db`
- **PostgreSQL**: `postgresql://user:password@host:port/dbname`

## 13. Deployment
The application is now ready for deployment. Access it at `http://localhost:5000` (local) or your EC2 IP.

## 🌟 Live AWS Resource Details (Mumbai ap-south-1)
Use these details to configure your production environment:

- **EC2 Public IP**: `15.206.145.174`
- **RDS Endpoint**: `terraform-20260126081643814700000001.cliumscw44qs.ap-south-1.rds.amazonaws.com`
- **S3 Bucket**: `smart-citizen-uploads-9d070998`
- **SNS Topic ARN**: `arn:aws:sns:ap-south-1:502713365215:smart-citizen-alerts`

### Quick Launch Command for EC2:
```bash
docker run -d -p 80:5000 \
  -e DATABASE_URL='postgresql://citizen_admin:password123@terraform-20260126081643814700000001.cliumscw44qs.ap-south-1.rds.amazonaws.com:5432/citizenreporter' \
  -e SECRET_KEY='your_manual_secret_here' \
  -e S3_BUCKET='smart-citizen-uploads-9d070998' \
  -e SNS_TOPIC_ARN='arn:aws:sns:ap-south-1:502713365215:smart-citizen-alerts' \
  smart-citizen-reporter:latest
```
