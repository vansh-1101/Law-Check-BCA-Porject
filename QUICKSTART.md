# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   setup.bat
   ```
   This will automatically:
   - Create virtual environment
   - Install all dependencies
   - Create necessary directories
   - Copy .env.example to .env

2. **Edit .env file** (optional for now - SQLite works out of the box)

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Create admin user:**
   ```bash
   # In a new terminal (keep the app running)
   python create_admin.py
   ```

5. **Open your browser:**
   ```
   http://127.0.0.1:5000
   ```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create .env file:**
   ```bash
   copy .env.example .env
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

5. **Create admin user:**
   ```bash
   python create_admin.py
   ```

## 📝 Default Login Credentials

### Admin Account
- **Email:** admin@legalconnect.in
- **Password:** admin123

⚠️ **Change this password immediately after first login!**

## ✅ Testing the Application

### 1. Register as Customer
1. Click "Register" in navigation
2. Fill form with role = "Customer"
3. Login with your credentials

### 2. Register as Lawyer
1. Open incognito window (or different browser)
2. Register with role = "Lawyer"
3. Login and setup profile

### 3. Verify Lawyer (as Admin)
1. Login as admin
2. Go to Admin Dashboard
3. Click "Pending Verifications"
4. Verify the lawyer

### 4. Book Consultation (as Customer)
1. Login as customer
2. Click "Browse Lawyers"
3. Select a verified lawyer
4. Book consultation

### 5. Test Messaging
1. Login as customer
2. Go to consultation details
3. Send a message
4. Login as lawyer
5. View and reply to message

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "Database locked"
**Solution:** Close all other instances of the app
```bash
# Stop the app (Ctrl+C)
# Delete the database
del instance\legal_platform.db
# Run again
python run.py
```

### Issue: "Port 5000 already in use"
**Solution:** Change port in run.py or kill the process
```bash
# Change port in run.py:
app.run(debug=True, host='127.0.0.1', port=5001)
```

## 📂 Project Structure

```
Law-Project/
├── app/                    # Application package
│   ├── routes/            # Route blueprints
│   ├── templates/         # HTML templates
│   ├── static/            # Static files
│   ├── models.py          # Database models
│   └── forms.py           # WTForms
├── instance/              # Database (auto-created)
├── venv/                  # Virtual environment
├── config.py              # Configuration
├── run.py                 # Entry point
└── requirements.txt       # Dependencies
```

## 🎯 Next Steps

1. ✅ Complete the remaining templates (browse lawyers, messaging, etc.)
2. ✅ Add more features (email notifications, file uploads)
3. ✅ Test all user flows
4. ✅ Migrate to MySQL for production
5. ✅ Deploy to a server

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/)

---

**Need help?** Check the main README.md for detailed documentation.
