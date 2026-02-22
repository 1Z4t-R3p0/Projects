# 🧠 How It Works: Smart Citizen Reporter

This document breaks down the technical architecture, logic, and cloud integrations of the Smart Citizen Reporter project. It serves as a comprehensive guide for technical interviews or portfolio reviews.

## 1. The Core Purpose
The Smart Citizen Reporter is a cloud-native platform designed to bridge the gap between civilians and municipal administration. It allows citizens to photograph and map civic issues (potholes, broken streetlights, water leaks, etc.) while providing administrators with a prioritized triage dashboard to manage repairs.

## 2. Cloud-Native Architecture (AWS)
The application is designed to mimic enterprise-scale, decoupled systems using Amazon Web Services:
*   **Compute (Docker + EC2)**: The core application is written in Python (Flask) and fully containerized via Docker. It is designed to be hosted on an AWS EC2 instance.
*   **Database (RDS - PostgreSQL)**: Instead of a flat-file database, it uses AWS RDS for relational, ACID-compliant data storage (User Auth, Issue Metadata, Status Tracking).
*   **Storage (S3)**: Processing heavy image uploads on the web server is an anti-pattern. Instead, images uploaded by citizens are streamed directly to an AWS S3 Bucket, reducing load on the EC2 instance and securing the media.

## 3. Artificial Intelligence Integration (AWS Rekognition)
The standout feature of this application is its automated triage system using Cloud AI.
*   When a citizen uploads a photo of an issue, the image is passed to **AWS Rekognition** (Amazon's Computer Vision API).
*   The AI scans the image and returns a list of detected labels and confidence scores.
*   **Threat Detection**: The backend cross-references these labels against an internal threat matrix. If the AI detects words like `fire`, `accident`, `flood`, or `collapsed building`, it overwrites the citizen's priority assessment and instantly flags the issue as **CRITICAL**.

## 4. Automated Alerting (AWS SNS)
Administrators cannot be expected to watch the dashboard 24/7. 
*   When the system (either via User Input or AI Image Classification) flags an issue as `CRITICAL`, it triggers an **Amazon Simple Notification Service (SNS)** pipeline.
*   SNS dispatches an immediate **SMS Text Message** or **Email** to the registered city administrators containing the incident location, description, and link, ensuring emergency response times are minimized.
*   *Fallback*: If AWS SNS is not configured during local testing, the system gracefully degrades to using standard SMTP (Flask-Mail) to send the alert.

## 5. Security & Fallbacks
*   **Graceful Degradation**: If the application cannot reach AWS (e.g., when running locally), it does not crash. It automatically falls back to local SQLite databases and local file system storage (`/static/uploads`), proving high fault-tolerance.
*   **Role-Based Access Control (RBAC)**: The application strictly partitions endpoints. Citizens cannot access the triage dashboard, and Admins cannot submit fake citizen reports.

## 6. Zero-Touch Deployment
The application includes automated Multi-Platform deployment scripts (`win-setup.ps1` and `wsl-setup.sh`) that encapsulate the Docker build process, allowing for 1-click execution on any platform.
