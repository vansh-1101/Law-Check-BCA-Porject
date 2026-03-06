# Database Storage & Checking Guide

## 📊 How Data is Stored

Your **Law Project** uses **SQLite** database - a file-based database system that stores all data in a single file.

### Database Location
```
c:\Users\darji\OneDrive\Desktop\Law-Project\instance\legal_platform.db
```

---

## 🗄️ Database Structure

Your database contains **6 tables**:

### 1. **users** - All User Accounts
Stores information about customers, lawyers, and admins.

**Fields:**
- `id` - Unique user ID
- `email` - User's email address
- `password_hash` - Encrypted password
- `full_name` - User's full name
- `phone` - Contact number
- `role` - User type (customer/lawyer/admin)
- `is_active` - Account status
- `created_at` - Registration date

### 2. **lawyer_profiles** - Lawyer Details
Extended information for lawyers only.

**Fields:**
- `bar_council_id` - Bar Council registration number
- `specializations` - Areas of expertise
- `experience_years` - Years of practice
- `education` - Educational qualifications
- `consultation_fee` - Consultation charges
- `verification_status` - pending/verified/rejected

### 3. **consultations** - Booking Records
Tracks all consultation bookings.

**Fields:**
- `customer_id` - Who booked
- `lawyer_id` - Which lawyer
- `consultation_date` - Appointment date/time
- `issue_description` - Problem description
- `category` - Type (civil/criminal/corporate)
- `status` - pending/confirmed/completed/cancelled

### 4. **messages** - Chat Messages
Messages between customers and lawyers.

**Fields:**
- `consultation_id` - Related consultation
- `sender_id` - Who sent the message
- `message` - Message content
- `is_read` - Read status

### 5. **legal_acts** - Indian Laws
Major legal acts (IPC, CrPC, etc.)

**Fields:**
- `name` - Full name of the act
- `short_name` - Abbreviation (e.g., "IPC")
- `year` - Year of enactment
- `category` - Criminal/Civil/Constitutional
- `total_sections` - Number of sections

### 6. **legal_sections** - Law Sections
Individual sections within each act.

**Fields:**
- `section_number` - Section number (e.g., "302", "498A")
- `title` - Section heading
- `description` - Full section text
- `keywords` - Search keywords
- `penalty` - Punishment details
- `is_bailable` - Can get bail?
- `is_cognizable` - Police can arrest without warrant?
- `is_compoundable` - Can settle out of court?

---

## 🔍 Current Database Contents

Based on the latest check:

### Statistics
- **Users:** 3
  - 1 Admin (admin@legalconnect.in)
  - 1 Lawyer (kabir@gmail.com)
  - 1 Customer (kabir12@gmail.com)
- **Lawyer Profiles:** 0
- **Consultations:** 0
- **Messages:** 0
- **Legal Acts:** 8
- **Legal Sections:** 41

### Legal Acts in Database
1. **IPC (1860)** - Indian Penal Code (511 sections)
2. **CrPC (1973)** - Code of Criminal Procedure (484 sections)
3. **Constitution (1950)** - Constitution of India (470 sections)
4. **Evidence Act (1872)** - Indian Evidence Act (167 sections)
5. **HMA (1955)** - Hindu Marriage Act (30 sections)
6. **Companies Act (2013)** - Companies Act (470 sections)
7. **IT Act (2000)** - Information Technology Act (94 sections)
8. **Consumer Act (2019)** - Consumer Protection Act (107 sections)

---

## 🛠️ Methods to Check Database

I've created **3 tools** for you to check your database:

### Method 1: Simple Command-Line Check ⭐ EASIEST
```bash
# Activate virtual environment and run
.\venv\Scripts\Activate.ps1
python simple_db_check.py
```

**What it shows:**
- Database statistics
- All users
- All legal acts
- Sample legal sections

### Method 2: Detailed Database Report
```bash
.\venv\Scripts\Activate.ps1
python check_database.py
```

**What it shows:**
- Complete details of all tables
- All records in each table
- Relationships between data

### Method 3: Web-Based Viewer 🌐 BEST FOR BROWSING
```bash
.\venv\Scripts\Activate.ps1
python view_database.py
```

Then open your browser and go to:
```
http://127.0.0.1:5001/db-viewer
```

**Features:**
- Beautiful web interface
- Color-coded data
- Easy to browse and search
- Shows all tables in organized format
- Real-time data display

---

## 💡 Using SQLite Browser (Optional)

You can also use **DB Browser for SQLite** - a free GUI tool:

1. **Download:** https://sqlitebrowser.org/
2. **Install** the application
3. **Open** the database file:
   ```
   c:\Users\darji\OneDrive\Desktop\Law-Project\instance\legal_platform.db
   ```
4. **Browse** all tables visually

---

## 📝 Quick Database Queries

If you want to run custom queries, you can use Python:

```python
from app import create_app, db
from app.models import User, LegalSection

app = create_app()
with app.app_context():
    # Get all users
    users = User.query.all()
    
    # Get specific user by email
    user = User.query.filter_by(email='admin@legalconnect.in').first()
    
    # Get all IPC sections
    ipc_sections = LegalSection.query.join(LegalAct).filter(
        LegalAct.short_name == 'IPC'
    ).all()
    
    # Count bailable offenses
    bailable_count = LegalSection.query.filter_by(is_bailable=True).count()
```

---

## 🔄 Database Management Commands

Your project includes these management scripts:

### Create Admin User
```bash
python create_admin.py
```

### Seed Legal Data
```bash
python seed_laws.py
```

### Migrate Database
```bash
python migrate_database.py
```

### Update Sections
```bash
python update_sections.py
```

---

## 📊 Data Relationships

```
User (Admin/Lawyer/Customer)
  ↓
  ├─→ LawyerProfile (if role=lawyer)
  ├─→ Consultations (as customer or lawyer)
  └─→ Messages (in consultations)

LegalAct (e.g., IPC)
  ↓
  └─→ LegalSections (e.g., Section 302, 420)
```

---

## 🎯 Recommended Workflow

**To check your database:**

1. **Quick Check:** Run `python simple_db_check.py`
2. **Detailed View:** Run `python view_database.py` and open browser
3. **Custom Queries:** Modify the scripts as needed

**To add data:**

1. Use the web application (run `python run.py`)
2. Or use the seed scripts
3. Or add via Python scripts

---

## ⚠️ Important Notes

1. **Backup:** The database file is in `instance/legal_platform.db` - back it up regularly
2. **Development:** You're using SQLite (good for development)
3. **Production:** For production, consider switching to MySQL/PostgreSQL (configured in `config.py`)
4. **Security:** Never commit the database file to Git (it's in `.gitignore`)

---

## 🆘 Troubleshooting

**If scripts don't work:**
1. Make sure virtual environment is activated
2. Check if database file exists in `instance/` folder
3. Run `python seed_laws.py` if database is empty

**If database is corrupted:**
1. Delete `instance/legal_platform.db`
2. Run `python run.py` to recreate
3. Run `python seed_laws.py` to populate

---

## 📞 Need Help?

Just ask me to:
- "Show me all users in database"
- "How many legal sections are there?"
- "Add a new user to database"
- "Export database to JSON"
- etc.
