from app import create_app, db
from models import User, Issue
from werkzeug.security import generate_password_hash
import random

app = create_app()

def seed_data():
    with app.app_context():
        db.create_all()
        
        # Check if data exists
        if User.query.first():
            print("Data already exists. Skipping seed.")
            return

        print("Creating Users...")
        # Create Admin
        admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
        
        # Create Citizens
        citizen1 = User(username='john_doe', password=generate_password_hash('password'), role='citizen')
        citizen2 = User(username='jane_smith', password=generate_password_hash('password'), role='citizen')
        
        db.session.add_all([admin, citizen1, citizen2])
        db.session.commit()
        
        print("Creating Issues...")
        issues_data = [
            ("Big Pothole on Main St", "There is a huge pothole damaging cars. This is an emergency.", "123 Main St", "Pending", citizen1, "sample_pothole.png"),
            ("Streetlight Broken", "Light pole #45 is flickering.", "45 Elm St", "Resolved", citizen1, None),
            ("Garbage Pile Up", "Trash hasn't been collected for 2 weeks.", "Sunset Blvd", "In Progress", citizen2, None),
            ("Water Leakage", "Pipe burst near the park.", "Central Park", "Pending", citizen2, None),
            ("Broken Sidewalk", "Dangerous for pedestrians.", "5th Avenue", "Pending", citizen1, None)
        ]
        
        issues = [Issue(title=t, description=d, location=l, status=s, author=a, image_file=i or 'default.jpg', priority=Issue.calculate_priority(d)) 
                  for t, d, l, s, a, i in issues_data]
        
        db.session.add_all(issues)
        db.session.commit()
        
        print("Seed data created successfully!")
        print("Admin: admin / admin123")
        print("Citizen: john_doe / password")
        print("Citizen: jane_smith / password")

if __name__ == '__main__':
    seed_data()
