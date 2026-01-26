from flask import Flask
from flask_login import LoginManager
from models import db, User, mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and Register Blueprints
from routes.auth_routes import auth_bp
from routes.citizen_routes import citizen_bp
from routes.admin_routes import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(citizen_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
