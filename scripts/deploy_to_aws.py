import subprocess
import os
import time

IP = "54.91.111.250"
KEY = "infra/deploy_key"
DB_HOST = "smart-citizen-reporter-db.cgd62y8so5ks.us-east-1.rds.amazonaws.com"
DB_PASS = "(Y{ZrCGQF=<DS4Oh"
BUCKET = "smart-citizen-reporter-uploads-3c8b4461"
SNS_ARN = "arn:aws:sns:us-east-1:502713365215:smart-citizen-reporter-critical-alerts"

def run_ssh(cmd):
    ssh_cmd = [
        "ssh", "-i", KEY, 
        "-o", "StrictHostKeyChecking=no",
        f"ubuntu@{IP}", cmd
    ]
    print(f"Running: {' '.join(ssh_cmd)}")
    return subprocess.run(ssh_cmd)

def deploy():
    # 1. Upload app
    print("Uploading app.tar.gz...")
    scp_cmd = [
        "scp", "-i", KEY,
        "-o", "StrictHostKeyChecking=no",
        "app.tar.gz", f"ubuntu@{IP}:/home/ubuntu/app.tar.gz"
    ]
    subprocess.run(scp_cmd)

    # 2. Extract and Setup
    setup_script = f"""
    set -e
    cd /home/ubuntu/app
    tar -xzf /home/ubuntu/app.tar.gz -C .
    
    # Ensure dependencies are installed
    sudo apt-get update
    sudo apt-get install -y pkg-config default-libmysqlclient-dev python3-dev build-essential
    
    # Create .env
    cat <<EOT > .env
DATABASE_URL=mysql://admin:{DB_PASS}@{DB_HOST}/citizenreporter
SECRET_KEY=prod_secret_key_998877
AWS_S3_BUCKET={BUCKET}
SNS_TOPIC_ARN={SNS_ARN}
AWS_REGION=us-east-1
EOT

    # Setup Venv
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install gunicorn cryptography mysqlclient boto3 Flask Flask-SQLAlchemy Flask-Login Flask-WTF email-validator Werkzeug
    # Alternatively try to install from requirements.txt but avoid mysqlclient if it fails
    pip install -r requirements.txt || true
    
    # Start app with Gunicorn
    pkill gunicorn || true
    nohup gunicorn -b 0.0.0.0:5000 app:app > app.log 2>&1 &
    """
    
    print("Running setup script on EC2...")
    run_ssh(setup_script)

if __name__ == "__main__":
    deploy()
