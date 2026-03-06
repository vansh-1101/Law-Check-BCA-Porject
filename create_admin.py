"""
Quick start script to create admin user
Run this after first setup to create an admin account
"""
from app import create_app, db
from app.models import User

def create_admin():
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@legalconnect.in').first()
        
        if existing_admin:
            print("❌ Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            email='admin@legalconnect.in',
            full_name='Admin User',
            role='admin',
            phone='+91 9999999999',
            is_active=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("\nLogin credentials:")
        print("Email: admin@legalconnect.in")
        print("Password: admin123")
        print("\n⚠️  Please change the password after first login!")

if __name__ == '__main__':
    create_admin()
