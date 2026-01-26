# AWS Deployment Guide (Free Tier Focus) ☁️

This guide outlines how to deploy the **Smart Citizen Issue Reporter** on Amazon Web Services (AWS) manually, staying within the **AWS Free Tier** limits as much as possible.

**Estimated Cost:** $0 (if you are eligible for the 12-month free tier).
**Services Used:** EC2 (t2.micro/t3.micro), RDS (db.t3.micro), S3 (Standard Storage), Elastic IP.

---

## 🏗️ Architecture Setup

1.  **EC2**: Hosting the Flask Application (Virtual Server).
2.  **RDS**: Hosting the PostgreSQL Database (Managed Database).
3.  **S3**: Storing uploaded Images (Object Storage).

---

## 🚀 Step 1: Launch an EC2 Instance (The Server)

1.  Log in to the **AWS Console**.
2.  Search for **EC2** and click **"Launch Instance"**.
3.  **Name**: `SmartCitizenServer`.
4.  **AMI**: Select **Ubuntu Server 24.04 LTS (HVM)** or 22.04 LTS (Free Tier Eligible).
5.  **Instance Type**: Select **t2.micro** or **t3.micro** (Free Tier Eligible).
6.  **Key Pair**: Create a new key pair (`smart-citizen-key`). **Download the .pem file** and keep it safe!
7.  **Network Settings**:
    -   Check "Allow SSH traffic from Anywhere" (0.0.0.0/0).
    -   Check "Allow HTTP traffic from the internet".
    -   Check "Allow HTTPS traffic from the internet".
8.  Click **Launch Instance**.
9.  Wait for the "Instance state" to turn **Running**.

---

## 🔒 Step 2: Configure RDS Database (Optional - Uses Free Tier)

*If you want to stick to SQLite to keep it simpler/safer, skip this and use the local file on EC2. But for Cloud Credits, use RDS.*

1.  Search for **RDS**.
2.  Click **Create database**.
3.  **Engine**: PostgreSQL.
4.  **Template**: Select **Free Tier**.
5.  **DB Instance Identifier**: `smart-citizen-db`.
6.  **Master Username**: `postgres`.
7.  **Master Password**: Set a strong password (e.g., `SecurePass123!`).
8.  **Instance Config**: `db.t3.micro` or `db.t4g.micro`.
9.  **Public Access**: **Yes** (Easier for testing, but secure via Security Groups).
10. Click **Create Database**.
11. Once created, copy the **Endpoint** (e.g., `smart-citizen-db.cx...us-east-1.rds.amazonaws.com`).

---

## 📦 Step 3: Deploy Code to EC2

1.  **Connect to EC2**:
    Open your terminal where the `.pem` key is.
    ```bash
    chmod 400 smart-citizen-key.pem
    ssh -i "smart-citizen-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
    ```

2.  **Install Dependencies on Server**:
    ```bash
    sudo apt update
    sudo apt install python3-pip python3-venv git nginx -y
    ```

3.  **Clone Project**:
    *You can upload your code to GitHub first, or copy it via SCP.*
    ```bash
    git clone https://github.com/<YOUR_GITHUB_OR_UPLOADED_ZIP>.git
    cd SmartCitizenReporter
    ```

4.  **Setup Virtual Env & Install**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install gunicorn psycopg2-binary
    ```

5.  **Run Application (Test Mode)**:
    ```bash
    # Set Config to Production (Optional: Update config.py first)
    export DATABASE_URL="postgresql://postgres:SecurePass123!@<RDS_ENDPOINT>:5432/postgres"
    
    # Run with Gunicorn
    gunicorn --bind 0.0.0.0:8000 app:app
    ```
    *Visit `http://<YOUR_EC2_PUBLIC_IP>:8000` in your browser. If it loads, you are live!*

---

## 🌐 Step 4: Keep It Running (Daemonize)

To keep the app running even after you exit SSH, use `systemd`.

1.  **Create Service File**:
    ```bash
    sudo nano /etc/systemd/system/smartcitizen.service
    ```
2.  **Paste Content**:
    ```ini
    [Unit]
    Description=Gunicorn instance to serve SmartCitizenReporter
    After=network.target

    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/SmartCitizenReporter
    Environment="PATH=/home/ubuntu/SmartCitizenReporter/venv/bin"
    Environment="DATABASE_URL=postgresql://postgres:SecurePass123!@<RDS_ENDPOINT>:5432/postgres"
    ExecStart=/home/ubuntu/SmartCitizenReporter/venv/bin/gunicorn --workers 3 --bind unix:smartcitizen.sock -m 007 app:app

    [Install]
    WantedBy=multi-user.target
    ```
3.  **Start Service**:
    ```bash
    sudo systemctl start smartcitizen
    sudo systemctl enable smartcitizen
    ```

---

## 🌍 Step 5: Configure Nginx (Reverse Proxy)

This makes your site accessible on Port 80 (standard HTTP) instead of 8000.

1.  **Create Config**:
    ```bash
    sudo nano /etc/nginx/sites-available/smartcitizen
    ```
2.  **Content**:
    ```nginx
    server {
        listen 80;
        server_name <YOUR_EC2_PUBLIC_IP>;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/SmartCitizenReporter/smartcitizen.sock;
        }
    }
    ```
3.  **Enable & Restart**:
    ```bash
    sudo ln -s /etc/nginx/sites-available/smartcitizen /etc/nginx/sites-enabled
    sudo systemctl restart nginx
    ```

**Done! Your project is now live on AWS Free Tier.** 🎉
