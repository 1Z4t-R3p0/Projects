# Smart Citizen Issue Reporter 🚦

A modern, cloud-native web application that empowers citizens to report civic issues (like potholes, broken streetlights, or garbage) directly to city administrators. Built with Python/Flask and deployed on AWS for scalability and reliability.

![Architecture Diagram](https://github.com/1Z4t-R3p0/Projects/raw/main/docs/assets/architecture.png)

## 🌟 Features

-   **User-Friendly Reporting**: Citizens can easily upload photos and report issues with location details.
-   **Admin Dashboard**: A centralized dashboard for city officials to view, manage, and update the status of reported issues.
-   **Critical Alerts**: Automatically detects high-priority issues (e.g., "emergency", "danger") and sends **instant SNS notifications** (SMS/Email) to administrators.
-   **Cloud Storage**: Securely stores issue images in **AWS S3**.
-   **Reliable Database**: Uses **AWS RDS (PostgreSQL)** for robust data management.
-   **Live Deployment**: Fully containerized with Docker and hosted on **AWS EC2**.

## 🏗️ Architecture

The application follows a standard N-tier architecture deployed on AWS:

1.  **Frontend/Backend**: Flask application running in a Docker container on an **EC2** instance.
2.  **Database**: Managed **PostgreSQL** database on **Amazon RDS**.
3.  **Storage**: Uploaded images are stored directly in an **S3 Bucket**.
4.  **Notifications**: **Amazon SNS** is triggered for critical issue alerts.
5.  **Processing**: **AWS Lambda** (ready for integration) can establish triggers on S3 uploads for image optimization.

## 🚀 Getting Started

### Prerequisites
-   Docker & Docker Compose
-   AWS Account (for cloud deployment)

### Local Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/1Z4t-R3p0/Projects.git SmartCitizenReporter
    cd SmartCitizenReporter
    ```
2.  Run with Docker Compose:
    ```bash
    docker-compose up --build
    ```
3.  Access the app at `http://localhost:5000`.

### AWS Deployment (Manual)
Please refer to the detailed [AWS Manual Setup Guide](docs/MANUAL_SETUP.md) for step-by-step instructions on creating the VPC, EC2, RDS, and S3 resources manually within the Free Tier.

## 🔑 Login Credentials

**Admin Portal**:
-   **Username**: `admin`
-   **Password**: `admin123`

**Citizen Portal (Test)**:
-   **Username**: `john_doe` or `jane_smith`
-   **Password**: `password`

## 🛠️ Tech Stack

-   **Backend**: Python, Flask, SQLAlchemy
-   **Database**: PostgreSQL / SQLite (local)
-   **Cloud**: AWS (EC2, S3, RDS, SNS, Lambda)
-   **DevOps**: Docker, Terraform (optional), Git

## 🚨 Critical Issue Trigger

The system automatically scans the description of reported issues. If keywords like **"emergency"**, **"danger"**, **"accident"**, or **"fatal"** are detected, the priority is set to **Critical**, and an **AWS SNS** alert is immediately dispatched to the admin team.

---
*Created by [1Z4t](https://github.com/1Z4t-R3p0)*
