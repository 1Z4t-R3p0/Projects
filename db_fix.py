from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            print("Starting DB migration...")
            # Use raw SQL to add missing columns to RDS
            db.session.execute(text("ALTER TABLE issue ADD COLUMN IF NOT EXISTS latitude VARCHAR(20)"))
            db.session.execute(text("ALTER TABLE issue ADD COLUMN IF NOT EXISTS longitude VARCHAR(20)"))
            db.session.execute(text("ALTER TABLE issue ADD COLUMN IF NOT EXISTS maps_link VARCHAR(255)"))
            db.session.commit()
            print("✅ Database migration successful!")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate()
