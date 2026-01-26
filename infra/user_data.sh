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

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
apt-get install -y git

# Clone the repository (replace with your actual repo URL)
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/SmartCitizenReporter.git || echo "Using local files"

# Build Docker image
cd /home/ubuntu/SmartCitizenReporter || mkdir -p /home/ubuntu/SmartCitizenReporter
cat > Dockerfile << 'DOCKERFILE_END'
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    pkg-config \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance && chmod 777 instance

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["sh", "-c", "python pre_start.py && gunicorn --bind 0.0.0.0:5000 app:app"]
DOCKERFILE_END

# Create requirements.txt
cat > requirements.txt << 'REQ_END'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
python-dotenv==1.0.0
requests==2.31.0
gunicorn==21.2.0
google-cloud-storage==2.13.0
Flask-Mail==0.9.1
boto3==1.34.0
psycopg2-binary==2.9.9
REQ_END

# Build the image
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
