#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
apt-get install -y docker.io
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

# Install Git
apt-get install -y git

# Clone the repository
cd /home/ubuntu
git clone https://github.com/1Z4t-R3p0/Projects.git SmartCitizenReporter
cd SmartCitizenReporter

# Build Docker image (Dockerfile already exists in repo)
docker build -t smart-citizen-reporter:latest .

# Run the container
docker run -d \
  -p 80:5000 \
  --name smart-citizen-app \
  --restart unless-stopped \
  -e DATABASE_URL='${DATABASE_URL}' \
  -e S3_BUCKET='${S3_BUCKET}' \
  -e SNS_TOPIC_ARN='${SNS_TOPIC_ARN}' \
  -e AWS_REGION='${AWS_REGION}' \
  -e SECRET_KEY='${SECRET_KEY}' \
  smart-citizen-reporter:latest

# Log completion
echo "Smart Citizen Reporter deployed successfully!" > /home/ubuntu/deployment.log
date >> /home/ubuntu/deployment.log
