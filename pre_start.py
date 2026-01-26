from app import app, db
from models import User, Issue
from werkzeug.security import generate_password_hash
import os
import time
from sqlalchemy.exc import OperationalError

def pre_start():
    with app.app_context():
        # 1. Connect to DB with retries
        retries = 10
        while retries > 0:
            try:
                db.create_all()
                print("Database connectivity verified and tables created.")
                break
            except OperationalError as e:
                print(f"Database not ready ({e}). Retrying in 5s... ({retries} left)")
                time.sleep(5)
                retries -= 1
        
        # 2. Seed Admin User and sample data if empty
        if not User.query.filter_by(username='admin').first():
            print("Seeding initial data...")
            admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
            citizen1 = User(username='john_doe', password=generate_password_hash('password'), role='citizen')
            db.session.add_all([admin, citizen1])
            
            pothole = Issue(
                title="Big Pothole on Main St", 
                description="There is a huge pothole damaging cars. This is an emergency.", 
                location="123 Main St", 
                status="Pending", 
                author=citizen1, 
                image_file="sample_pothole.png",
                priority="Critical"
            )
            db.session.add(pothole)
            db.session.commit()
            print("Seed data created: Admin (admin/admin123)")
        else:
            print("Admin user already exists. Skipping seed.")

    # 3. Ensure upload directory exists
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        print(f"Created upload folder: {upload_path}")

if __name__ == '__main__':
    pre_start()
