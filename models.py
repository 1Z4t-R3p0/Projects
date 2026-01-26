from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_mail import Mail
from datetime import datetime

db = SQLAlchemy()
mail = Mail()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='citizen') # 'citizen' or 'admin'
    issues = db.relationship('Issue', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.role}')"

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(255), nullable=True, default='default.jpg') # Filename/URL
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    maps_link = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Pending') # Pending, In Progress, Resolved
    priority = db.Column(db.String(20), nullable=False, default='Low')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def calculate_priority(title, description):
        text = (str(title) + " " + str(description)).lower()
        # Critical priority keywords
        if any(word in text for word in ['emergency', 'danger', 'immediate', 'fatal', 'accident', 'fire', 'flood', 'critical', 'blast', 'explosion']):
            return 'Critical'
        # High priority keywords
        if any(word in text for word in ['repair', 'broken', 'damage', 'leaking', 'urgent', 'pothole', 'sewage', 'collapsed']):
            return 'High'
        # Medium priority keywords
        if any(word in text for word in ['garbage', 'trash', 'light', 'noise', 'parking', 'animal']):
            return 'Medium'
        return 'Low'

    def __repr__(self):
        return f"Issue('{self.title}', '{self.status}')"
