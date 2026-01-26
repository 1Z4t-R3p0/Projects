# Smart Citizen Issue Reporter 🏙️

A cloud-based web application that connects citizens with authorities to solve public issues efficiently. This is a Final Year Project demonstrating Full Stack Development and Cloud Computing concepts.

## 🌟 Features

### For Citizens:
- **User Registration & Login**: Secure account creation.
- **Report Issues**: Upload photos, location, and description of issues (Garbage, Potholes, etc.).
- **Track Status**: View the status of reported issues (Pending, In Progress, Resolved).

### For Authorities (Admin):
- **Admin Dashboard**: Overview of total reports and statistics.
- **Manage Issues**: View all incoming reports and update their status.
- **Delete Reports**: Remove duplicate or fake reports.

## 🛠️ Technology Stack

- **Backend**: Python (Flask), Flask-SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Templates)
- **Database**: SQLite (Local) / Cloud SQL (Production)
- **Cloud Platform**: Google Cloud Platform (Cloud Run, Cloud Storage)

## 🚀 How to Run Locally

1. **Clone the repository/Open project folder**:
   ```bash
   cd SmartCitizenReporter
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the App**:
   Open http://127.0.0.1:5000 in your browser.

## ☁️ Cloud Deployment (Google Cloud)

This project is ready to be deployed on Google Cloud Run.

1. **Build the Container Image**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/smart-citizen-reporter
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy smart-citizen-reporter --image gcr.io/PROJECT-ID/smart-citizen-reporter --platform managed --region us-central1 --allow-unauthenticated
   ```

## 🏗️ AWS Cloud Architecture (Alternative)

If deploying to Amazon Web Services (AWS), the architecture utilizes the following services for scalability and reliability:

### Architecture Diagram Text Description:

**[User/Citizen]**  
   ⬇️ *(HTTPS Request)*  
**[Route 53]** *(DNS Management)*  
   ⬇️  
**[AWS Elastic Beanstalk]** *(Application PaaS)*  
   ┣━━ **[EC2 Instances]** *(Auto-scaling Group)*: Runs the Flask Application  
   ┃      ┗━━ **Docker Container**: Hosts the web server (Gunicorn)  
   ┣━━ **[Application Load Balancer]**: Distributes traffic  
   ⬇️  
**[Backend Services]**  
   ┣━━ **[Amazon RDS]** *(PostgreSQL)*: Stores User data, Issues, and Metadata.  
   ┗━━ **[Amazon S3]** *(Simple Storage Service)*: Stores uploaded issue images safely and reliably.

### Why this Architecture?
1.  **Elastic Beanstalk**: Manages the deployment details (capacity provisioning, load balancing, auto-scaling) so we can focus on code.
2.  **RDS**: Managed relational database service that creates backups and patches automatically.
3.  **S3**: Highly durable storage for images, cheaper and more reliable than storing on the web server disk.

## 🔮 Future Enhancements

To further scale this project, the following advanced features can be implemented:

1.  **AI-Based Automatic Categorization**:
    -   Use **TensorFlow/Keras** or **Google Vision API** to analyze uploaded images and automatically detect if it's a pothole, garbage, etc.
    -   Prevents users from selecting the wrong category.

2.  **GIS Integration (Google Maps API)**:
    -   Replace the text-based location with an interactive map.
    -   Allow users to "Pin" their location to get exact GPS coordinates.
    -   Show a heat map of issues for authorities.

3.  **Automated Duplicate Detection**:
    -   Use image hashing (perceptual hash) to check if the same photo has already been uploaded.
    -   Check if an issue exists within a 10-meter radius of a new report.

4.  **Real-time Notifications**:
    -   Integrate **Twilio** (SMS) or **SendGrid** (Email) to notify citizens when their issue status changes from "Pending" to "Resolved".

## 📂 Project Structure

- `app.py`: Main application entry point.
- `models.py`: Database classes (User, Issue).
- `routes/`: Contains logic for Auth, Citizen, and Admin modules.
- `templates/`: HTML files for valid pages.
- `static/`: CSS styles and uploaded images.

## 🎓 Final Year Viva Explanations

**Q: Why Flask?**
A: Flask is lightweight, easy to learn, and perfect for prototyping RESTful web applications.

**Q: How is it secure?**
A: Passwords are hashed using `werkzeug.security`. We use Session-based authentication via `Flask-Login` and secure file handling for uploads.

**Q: What is the Cloud component?**
A: The application is containerized using Docker and runs on Google Cloud Run (Serverless). It is scalable and cost-effective.

---
**Developed by [Your Name]**
