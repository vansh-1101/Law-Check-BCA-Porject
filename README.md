# LegalConnect India - Legal Consultation Platform

A Flask-based web application connecting customers with verified lawyers across India.

## 🎯 Project Overview

This is a BCA final year project that demonstrates a full-stack web application for legal consultation services. The platform allows customers to browse verified lawyers, book consultations, and communicate through a secure messaging system.

## 🛠️ Technology Stack

- **Backend:** Python 3.10+ with Flask framework
- **Database:** SQLite (development) / MySQL (production)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Authentication:** Flask-Login with bcrypt password hashing
- **Forms:** Flask-WTF with WTForms validation
- **Email:** Flask-Mail for notifications

## 📋 Features

### For Customers
- Browse verified lawyers by specialization
- Filter lawyers by experience, fees, and category
- Book consultations with preferred lawyers
- Direct messaging with lawyers
- View consultation history and status

### For Lawyers
- Create and manage professional profile
- Upload credentials and documents
- Manage consultation requests
- Communicate with clients
- Track consultation history

### For Admins
- Verify lawyer credentials
- Manage users (activate/deactivate)
- View platform statistics
- Monitor consultations

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- MySQL (for production) or SQLite (for development)

### Setup Steps

1. **Clone the repository**
```bash
cd Law-Project
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy the example env file
copy .env.example .env

# Edit .env file with your settings
# For development, you can use SQLite (default)
# For production, configure MySQL connection
```

5. **Initialize database**
```bash
# The database will be created automatically on first run
python run.py
```

6. **Create admin user (optional)**
```python
# Open Python shell
python

# Run these commands:
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        email='admin@legalconnect.in',
        full_name='Admin User',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    print("Admin user created!")
```

7. **Run the application**
```bash
python run.py
```

8. **Access the application**
```
Open your browser and go to: http://127.0.0.1:5000
```

## 📁 Project Structure

```
Law-Project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main pages
│   │   ├── customer.py      # Customer routes
│   │   ├── lawyer.py        # Lawyer routes
│   │   └── admin.py         # Admin routes
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── auth/            # Auth templates
│   │   ├── main/            # Main pages
│   │   ├── customer/        # Customer templates
│   │   ├── lawyer/          # Lawyer templates
│   │   └── admin/           # Admin templates
│   └── static/              # Static files
│       ├── css/             # CSS files
│       ├── js/              # JavaScript files
│       └── uploads/         # User uploads
├── instance/                # Instance folder (database)
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🎨 Design System

The application uses a professional legal-themed design system:

- **Primary Color:** Supreme Navy (#0F172A)
- **Success Color:** Verdict Green (#15803D)
- **Accent Color:** Seal Red (#9A3412)
- **Background:** Legal Pad (#F8FAFC)

**Typography:**
- Headings: Playfair Display (serif)
- Body: Manrope (sans-serif)
- Mono: JetBrains Mono (for case numbers, dates)

## 🔐 Default Credentials

After creating the admin user (step 6 above):
- **Email:** admin@legalconnect.in
- **Password:** admin123

**⚠️ Change these credentials immediately after first login!**

## 📊 Database Schema

### Users Table
- id, email, password_hash, full_name, phone, role, is_active, created_at

### Lawyer Profiles Table
- id, user_id, bar_council_id, specializations, experience_years, education, languages, consultation_fee, verification_status, bio, profile_image, credentials_document

### Consultations Table
- id, customer_id, lawyer_id, consultation_date, issue_description, category, status, created_at

### Messages Table
- id, consultation_id, sender_id, message, is_read, created_at

## 🧪 Testing

To test the application:

1. Register as a customer
2. Register as a lawyer (separate account)
3. Login as admin and verify the lawyer
4. Login as customer and browse lawyers
5. Book a consultation
6. Test messaging between customer and lawyer

## 🚀 Deployment

### For Production (MySQL)

1. Install MySQL and create database:
```sql
CREATE DATABASE legal_platform;
CREATE USER 'legal_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON legal_platform.* TO 'legal_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Update `.env` file:
```
DATABASE_URL=mysql+pymysql://legal_user:your_password@localhost/legal_platform
```

3. Run the application:
```bash
python run.py
```

## 📝 License

This project is created for educational purposes as a BCA final year project.

## 👨‍💻 Author

Created by Vansh Darji for BCA Final Year Project

## 🙏 Acknowledgments

- Flask documentation
- Tailwind CSS
- All open-source libraries used in this project
