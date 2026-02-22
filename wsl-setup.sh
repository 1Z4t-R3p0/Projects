#!/bin/bash
set -e

# ====================================
#   Smart Citizen Reporter Deployment (WSL/Linux)
# ====================================

REPO_URL="https://github.com/1Z4t-R3p0/Projects.git"
PROJECT_DIR="$HOME/Smart-Citizen-Reporter"

echo "===================================="
echo "   Smart Citizen Reporter Setup"
echo "===================================="

# 1. Install Git and standard dependencies
if ! command -v git >/dev/null 2>&1; then
    echo "Installing Git..."
    sudo apt-get update && sudo apt-get install -y git curl
fi

# 2. Install Docker if missing
if ! command -v docker >/dev/null 2>&1; then
    echo "Docker not found. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker "$USER"
    echo "Docker installed! You may need to log out and back in for permissions to take effect."
fi

# Ensure Docker daemon is running
if ! sudo docker info >/dev/null 2>&1; then
    echo "Starting Docker daemon..."
    sudo service docker start || sudo dockerd &
    sleep 3
fi

# 3. Clone or Update Project
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning project repository..."
    git clone "$REPO_URL" "$PROJECT_DIR"
else
    echo "Project exists at $PROJECT_DIR. Pulling latest changes..."
    cd "$PROJECT_DIR" || exit
    git pull
fi

# 4. Run Docker Compose
cd "$PROJECT_DIR" || exit
echo "Starting the Smart Citizen Reporter..."
sudo docker compose up -d --build || sudo docker-compose up -d --build

echo ""
echo "===================================="
echo " Deployment Complete!"
echo " Access Application at: http://localhost:5000"
echo " Admin Credentials: admin / admin123"
echo " Citizen Credentials: john_doe / password"
echo "===================================="
