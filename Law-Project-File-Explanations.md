# Law Check Project - Complete File Structure Explanation

## 📁 Project Overview

This document explains **every file** in your Law Check project, what it does, what's inside, and how it connects with other files.

---

## 🗂️ Project Directory Structure

```
Law-Project/
├── 📄 Root Configuration Files
│   ├── run.py                    # Main entry point
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt          # Python dependencies
│   ├── setup.bat                 # Windows setup script
│   ├── create_admin.py           # Admin user creation script
│   ├── seed_laws.py              # Database seeding for laws
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore rules
│   ├── README.md                 # Project documentation
│   └── QUICKSTART.md             # Quick start guide
│
├── 📁 app/                       # Main application package
│   ├── __init__.py               # App factory & initialization
│   ├── models.py                 # Database models
│   ├── forms.py                  # Form definitions
│   │
│   ├── 📁 routes/                # Route blueprints
│   │   ├── __init__.py
│   │   ├── main.py               # Public pages (home, about, laws)
│   │   ├── auth.py               # Login/Register
│   │   ├── customer.py           # Customer dashboard & features
│   │   ├── lawyer.py             # Lawyer dashboard & features
│   │   └── admin.py              # Admin panel
│   │
│   ├── 📁 templates/             # HTML templates
│   │   ├── base.html             # Base template (header, footer)
│   │   ├── 📁 main/              # Public pages
│   │   ├── 📁 auth/              # Login/Register pages
│   │   ├── 📁 customer/          # Customer pages
│   │   ├── 📁 lawyer/            # Lawyer pages
│   │   └── 📁 admin/             # Admin pages
│   │
│   └── 📁 static/                # Static files (CSS, JS, images)
│       ├── 📁 css/
│       ├── 📁 js/
│       └── 📁 uploads/           # User uploaded files
│
├── 📁 instance/                  # Instance-specific files
│   └── legal_platform.db         # SQLite database
│
└── 📁 venv/                      # Virtual environment (Python packages)
```

---

## 📄 ROOT LEVEL FILES

---

### 1. `run.py` - Application Entry Point

**Purpose:** Starts the Flask web server

**What's Inside:**
```python
# Imports
from app import create_app, db
from app.models import User, LawyerProfile, Consultation, Message

# Create Flask app
app = create_app(os.getenv('FLASK_ENV') or 'development')

# Shell context (for Flask shell commands)
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, ...}

# Main execution
if __name__ == '__main__':
    # Create instance folder
    # Run app on http://127.0.0.1:5000
    app.run(debug=True, host='127.0.0.1', port=5000)
```

**How to Use:**
```bash
python run.py
```

**What Happens:**
1. Creates Flask application using factory pattern
2. Sets up database models in Flask shell
3. Creates `instance/` folder if missing
4. Starts development server on port 5000
5. Enables debug mode (auto-reload on code changes)

---

### 2. `config.py` - Configuration Settings

**Purpose:** Centralized configuration for different environments

**What's Inside:**

#### Base Config Class
```python
class Config:
    # Security
    SECRET_KEY = 'dev-secret-key-change-this'
    
    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/legal_platform.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Uploads
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
    
    # Email (for future use)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
    # Pagination
    ITEMS_PER_PAGE = 10
    
    # Session
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
```

#### Environment-Specific Configs
```python
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

**How It's Used:**
- `run.py` loads config based on `FLASK_ENV` variable
- Development mode by default
- Can switch to production for deployment

---

### 3. `requirements.txt` - Python Dependencies

**Purpose:** Lists all Python packages needed

**What's Inside:**
```
Flask==3.0.0              # Web framework
Flask-SQLAlchemy==3.1.1   # Database ORM
Flask-Login==0.6.3        # User authentication
Flask-Mail==0.9.1         # Email support
Flask-Migrate==4.0.5      # Database migrations
Flask-WTF==1.2.1          # Form handling
WTForms==3.1.1            # Form validation
python-dotenv==1.0.0      # Environment variables
email-validator==2.1.0    # Email validation
```

**How to Use:**
```bash
pip install -r requirements.txt
```

---

### 4. `setup.bat` - Windows Setup Script

**Purpose:** Automated setup for Windows users

**What It Does:**
1. Creates virtual environment (`venv`)
2. Activates virtual environment
3. Installs all dependencies from `requirements.txt`
4. Creates database tables
5. Prompts to create admin user

**How to Use:**
```bash
setup.bat
```

---

### 5. `create_admin.py` - Admin User Creation

**Purpose:** Creates the first admin account

**What's Inside:**
```python
def create_admin():
    # Check if admin exists
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
```

**Default Credentials:**
- Email: `admin@legalconnect.in`
- Password: `admin123`

**How to Use:**
```bash
python create_admin.py
```

---

### 6. `seed_laws.py` - Legal Database Seeding

**Purpose:** Populates database with Indian laws

**What's Inside:**
```python
def seed_laws():
    # Clear existing data
    LegalSection.query.delete()
    LegalAct.query.delete()
    
    # Add 8 major Indian acts
    acts = [
        {
            'name': 'Indian Penal Code',
            'short_name': 'IPC',
            'year': 1860,
            'category': 'Criminal',
            'description': '...',
            'sections': [
                {'section_number': '302', 'title': 'Murder', ...},
                {'section_number': '420', 'title': 'Cheating', ...},
                # ... 10 sections
            ]
        },
        # ... 7 more acts
    ]
    
    # Insert into database
    for act_data in acts:
        act = LegalAct(...)
        db.session.add(act)
        
        for section_data in act_data['sections']:
            section = LegalSection(...)
            db.session.add(section)
    
    db.session.commit()
```

**Content Added:**
- 8 Legal Acts (IPC, CrPC, Constitution, etc.)
- 41 Sections with descriptions
- Searchable keywords

**How to Use:**
```bash
python seed_laws.py
```

---

### 7. `.env.example` - Environment Variables Template

**Purpose:** Template for sensitive configuration

**What's Inside:**
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///instance/legal_platform.db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
FLASK_ENV=development
```

**How to Use:**
1. Copy to `.env`: `cp .env.example .env`
2. Fill in actual values
3. Never commit `.env` to Git (it's in `.gitignore`)

---

### 8. `README.md` - Project Documentation

**Purpose:** Main project documentation

**What's Inside:**
- Project description
- Features list
- Installation instructions
- Usage guide
- Technology stack
- Screenshots
- License

---

### 9. `QUICKSTART.md` - Quick Start Guide

**Purpose:** Fast setup instructions

**What's Inside:**
- Prerequisites
- Step-by-step setup
- Common commands
- Troubleshooting

---

## 📁 APP FOLDER (`app/`)

---

### 10. `app/__init__.py` - Application Factory

**Purpose:** Creates and configures Flask application

**What's Inside:**

#### 1. Extension Initialization
```python
# Initialize Flask extensions
db = SQLAlchemy()           # Database
login_manager = LoginManager()  # User authentication
mail = Mail()               # Email
migrate = Migrate()         # Database migrations
```

#### 2. Application Factory Function
```python
def create_app(config_name='development'):
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprints (route modules)
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.customer import customer_bp
    from app.routes.lawyer import lawyer_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(lawyer_bp)
    app.register_blueprint(admin_bp)
    
    # Register template filters
    @app.template_filter('from_json')
    def from_json_filter(value):
        return json.loads(value) if value else []
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
```

**Key Concepts:**

**Application Factory Pattern:**
- Function that creates and returns Flask app
- Allows multiple app instances (testing, production)
- Cleaner than global app object

**Blueprints:**
- Modular route organization
- Each blueprint handles specific functionality
- Registered with `app.register_blueprint()`

**Extensions:**
- Initialized once, then attached to app
- Allows reuse across multiple apps

---

### 11. `app/models.py` - Database Models

**Purpose:** Defines database structure (tables and relationships)

**What's Inside:**

#### 1. User Model
```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), nullable=False)  # customer, lawyer, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lawyer_profile = db.relationship('LawyerProfile', backref='user', uselist=False)
    customer_consultations = db.relationship('Consultation', foreign_keys='Consultation.customer_id', backref='customer')
    lawyer_consultations = db.relationship('Consultation', foreign_keys='Consultation.lawyer_id', backref='lawyer')
    
    # Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

**Relationships Explained:**
- `lawyer_profile`: One user can have one lawyer profile (1-to-1)
- `customer_consultations`: One customer can have many consultations (1-to-many)
- `lawyer_consultations`: One lawyer can have many consultations (1-to-many)

#### 2. LawyerProfile Model
```python
class LawyerProfile(db.Model):
    __tablename__ = 'lawyer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bar_council_id = db.Column(db.String(50), unique=True, nullable=False)
    specializations = db.Column(db.String(200))  # JSON array
    experience_years = db.Column(db.Integer)
    education = db.Column(db.Text)
    languages = db.Column(db.String(100))
    consultation_fee = db.Column(db.Float)
    bio = db.Column(db.Text)
    verification_status = db.Column(db.String(20), default='pending')
    # ... more fields
```

#### 3. Consultation Model
```python
class Consultation(db.Model):
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lawyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    consultation_date = db.Column(db.DateTime, nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    # ... more fields
    
    # Relationship
    messages = db.relationship('Message', backref='consultation', lazy='dynamic')
```

#### 4. Message Model
```python
class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

#### 5. LegalAct Model
```python
class LegalAct(db.Model):
    __tablename__ = 'legal_acts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    short_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    total_sections = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    sections = db.relationship('LegalSection', backref='act', lazy='dynamic')
```

#### 6. LegalSection Model
```python
class LegalSection(db.Model):
    __tablename__ = 'legal_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    act_id = db.Column(db.Integer, db.ForeignKey('legal_acts.id'))
    section_number = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Database Relationships Diagram:**
```
User (1) ←→ (1) LawyerProfile
User (1) ←→ (many) Consultation (as customer)
User (1) ←→ (many) Consultation (as lawyer)
Consultation (1) ←→ (many) Message
LegalAct (1) ←→ (many) LegalSection
```

---

### 12. `app/forms.py` - Form Definitions

**Purpose:** Defines and validates HTML forms

**What's Inside:**

#### 1. RegistrationForm
```python
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    role = SelectField('Register as', choices=[('customer', 'Customer'), ('lawyer', 'Lawyer')])
    
    def validate_email(self, email):
        # Custom validation: check if email exists
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')
```

**Validators:**
- `DataRequired()`: Field cannot be empty
- `Email()`: Must be valid email format
- `Length(min=6)`: Minimum 6 characters
- `EqualTo('password')`: Must match password field
- Custom `validate_email()`: Checks database for duplicates

#### 2. LoginForm
```python
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
```

#### 3. LawyerProfileForm
```python
class LawyerProfileForm(FlaskForm):
    bar_council_id = StringField('Bar Council ID', validators=[DataRequired()])
    specializations = StringField('Specializations (comma-separated)')
    experience_years = IntegerField('Years of Experience')
    education = TextAreaField('Education')
    languages = StringField('Languages')
    consultation_fee = FloatField('Consultation Fee (₹)')
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    credentials_document = FileField('Credentials', validators=[FileAllowed(['pdf', 'doc', 'docx'])])
```

#### 4. ConsultationBookingForm
```python
class ConsultationBookingForm(FlaskForm):
    lawyer_id = SelectField('Select Lawyer', coerce=int)
    consultation_date = DateTimeField('Date & Time', format='%Y-%m-%dT%H:%M')
    category = SelectField('Category', choices=[
        ('civil', 'Civil Law'),
        ('criminal', 'Criminal Law'),
        ('corporate', 'Corporate Law'),
        # ... more choices
    ])
    issue_description = TextAreaField('Describe Your Issue', validators=[Length(min=20, max=1000)])
```

#### 5. MessageForm
```python
class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
```

**How Forms Work:**
1. **Backend (routes):** Create form instance
2. **Template:** Render form fields
3. **User:** Fills and submits form
4. **Backend:** Validates data
5. **If valid:** Process data (save to database)
6. **If invalid:** Show error messages

---

## 📁 ROUTES FOLDER (`app/routes/`)

Routes are organized into **blueprints** (modules) by functionality.

---

### 13. `app/routes/main.py` - Public Pages

**Purpose:** Routes accessible to everyone (no login required)

**What's Inside:**

#### Route 1: Home Page
```python
@main_bp.route('/')
def index():
    # Get statistics
    total_lawyers = User.query.filter_by(role='lawyer').count()
    verified_lawyers = LawyerProfile.query.filter_by(verification_status='verified').count()
    total_customers = User.query.filter_by(role='customer').count()
    
    return render_template('main/index.html',
                         total_lawyers=total_lawyers,
                         verified_lawyers=verified_lawyers,
                         total_customers=total_customers)
```

#### Route 2: About Page
```python
@main_bp.route('/about')
def about():
    return render_template('main/about.html')
```

#### Route 3: Contact Page
```python
@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')
```

#### Route 4: Browse Laws
```python
@main_bp.route('/browse-laws')
def browse_laws():
    # Get query parameters
    category = request.args.get('category', 'all')
    search_query = request.args.get('q', '')
    
    # Filter acts
    query = LegalAct.query
    if category != 'all':
        query = query.filter_by(category=category)
    if search_query:
        query = query.filter(LegalAct.name.ilike(f'%{search_query}%'))
    
    acts = query.all()
    total_acts = LegalAct.query.count()
    total_sections = LegalSection.query.count()
    
    return render_template('main/browse_laws.html',
                         acts=acts,
                         total_acts=total_acts,
                         total_sections=total_sections,
                         selected_category=category)
```

#### Route 5: View Act
```python
@main_bp.route('/browse-laws/act/<int:act_id>')
def view_act(act_id):
    act = LegalAct.query.get_or_404(act_id)
    sections = act.sections.all()
    related_acts = LegalAct.query.filter_by(category=act.category).limit(3).all()
    
    return render_template('main/view_act.html',
                         act=act,
                         sections=sections,
                         related_acts=related_acts)
```

#### Route 6: View Section
```python
@main_bp.route('/browse-laws/section/<int:section_id>')
def view_section(section_id):
    section = LegalSection.query.get_or_404(section_id)
    act = section.act
    
    # Get previous and next sections
    prev_section = LegalSection.query.filter(
        LegalSection.act_id == act.id,
        LegalSection.id < section_id
    ).order_by(LegalSection.id.desc()).first()
    
    next_section = LegalSection.query.filter(
        LegalSection.act_id == act.id,
        LegalSection.id > section_id
    ).order_by(LegalSection.id.asc()).first()
    
    return render_template('main/view_section.html',
                         section=section,
                         act=act,
                         prev_section=prev_section,
                         next_section=next_section)
```

#### Route 7: Search Laws API (AJAX)
```python
@main_bp.route('/api/search-laws')
def search_laws():
    query = request.args.get('q', '')
    
    # Search in acts
    acts = LegalAct.query.filter(
        or_(
            LegalAct.name.ilike(f'%{query}%'),
            LegalAct.short_name.ilike(f'%{query}%')
        )
    ).limit(5).all()
    
    # Search in sections
    sections = LegalSection.query.filter(
        or_(
            LegalSection.title.ilike(f'%{query}%'),
            LegalSection.section_number.ilike(f'%{query}%'),
            LegalSection.keywords.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    # Return JSON
    return jsonify({
        'acts': [{'id': a.id, 'name': a.name, 'short_name': a.short_name} for a in acts],
        'sections': [{'id': s.id, 'title': s.title, 'section_number': s.section_number} for s in sections]
    })
```

---

### 14. `app/routes/auth.py` - Authentication

**Purpose:** Login, register, logout

**What's Inside:**

#### Route 1: Register
```python
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Create new user
        user = User(
            email=form.email.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)
```

#### Route 2: Login
```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'lawyer':
                return redirect(url_for('lawyer.dashboard'))
            else:
                return redirect(url_for('customer.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)
```

#### Route 3: Logout
```python
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
```

---

### 15. `app/routes/customer.py` - Customer Features

**Purpose:** Customer dashboard, browse lawyers, book consultations

**What's Inside:**

#### Route 1: Customer Dashboard
```python
@customer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'customer':
        abort(403)
    
    # Get customer's consultations
    consultations = Consultation.query.filter_by(
        customer_id=current_user.id
    ).order_by(Consultation.created_at.desc()).all()
    
    return render_template('customer/dashboard.html',
                         consultations=consultations)
```

#### Route 2: Browse Lawyers
```python
@customer_bp.route('/browse-lawyers')
@login_required
def browse_lawyers():
    # Get filters
    specialization = request.args.get('specialization')
    min_experience = request.args.get('min_experience', type=int)
    
    # Query lawyers
    query = LawyerProfile.query.filter_by(verification_status='verified')
    
    if specialization:
        query = query.filter(LawyerProfile.specializations.ilike(f'%{specialization}%'))
    if min_experience:
        query = query.filter(LawyerProfile.experience_years >= min_experience)
    
    lawyers = query.all()
    
    return render_template('customer/browse_lawyers.html',
                         lawyers=lawyers)
```

#### Route 3: Book Consultation
```python
@customer_bp.route('/book-consultation/<int:lawyer_id>', methods=['GET', 'POST'])
@login_required
def book_consultation(lawyer_id):
    lawyer = User.query.get_or_404(lawyer_id)
    form = ConsultationBookingForm()
    
    if form.validate_on_submit():
        consultation = Consultation(
            customer_id=current_user.id,
            lawyer_id=lawyer_id,
            consultation_date=form.consultation_date.data,
            category=form.category.data,
            issue_description=form.issue_description.data,
            status='pending'
        )
        
        db.session.add(consultation)
        db.session.commit()
        
        flash('Consultation booked successfully!', 'success')
        return redirect(url_for('customer.dashboard'))
    
    return render_template('customer/book_consultation.html',
                         form=form,
                         lawyer=lawyer)
```

#### Route 4: View Consultation
```python
@customer_bp.route('/consultation/<int:consultation_id>')
@login_required
def view_consultation(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    # Check authorization
    if consultation.customer_id != current_user.id:
        abort(403)
    
    messages = consultation.messages.order_by(Message.created_at).all()
    form = MessageForm()
    
    return render_template('customer/view_consultation.html',
                         consultation=consultation,
                         messages=messages,
                         form=form)
```

#### Route 5: Send Message
```python
@customer_bp.route('/consultation/<int:consultation_id>/send-message', methods=['POST'])
@login_required
def send_message(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    form = MessageForm()
    
    if form.validate_on_submit():
        message = Message(
            consultation_id=consultation_id,
            sender_id=current_user.id,
            message=form.message.data
        )
        
        db.session.add(message)
        db.session.commit()
        
        flash('Message sent!', 'success')
    
    return redirect(url_for('customer.view_consultation',
                          consultation_id=consultation_id))
```

---

### 16. `app/routes/lawyer.py` - Lawyer Features

**Purpose:** Lawyer dashboard, profile setup, manage consultations

**What's Inside:**

#### Route 1: Lawyer Dashboard
```python
@lawyer_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'lawyer':
        abort(403)
    
    # Get lawyer's consultations
    consultations = Consultation.query.filter_by(
        lawyer_id=current_user.id
    ).order_by(Consultation.consultation_date.desc()).all()
    
    # Get statistics
    total_consultations = len(consultations)
    pending_consultations = len([c for c in consultations if c.status == 'pending'])
    completed_consultations = len([c for c in consultations if c.status == 'completed'])
    
    return render_template('lawyer/dashboard.html',
                         consultations=consultations,
                         total_consultations=total_consultations,
                         pending_consultations=pending_consultations,
                         completed_consultations=completed_consultations)
```

#### Route 2: Setup Profile
```python
@lawyer_bp.route('/setup-profile', methods=['GET', 'POST'])
@login_required
def setup_profile():
    if current_user.role != 'lawyer':
        abort(403)
    
    form = LawyerProfileForm()
    
    if form.validate_on_submit():
        # Check if profile exists
        profile = current_user.lawyer_profile
        
        if not profile:
            profile = LawyerProfile(user_id=current_user.id)
        
        # Update profile
        profile.bar_council_id = form.bar_council_id.data
        profile.specializations = form.specializations.data
        profile.experience_years = form.experience_years.data
        profile.education = form.education.data
        profile.languages = form.languages.data
        profile.consultation_fee = form.consultation_fee.data
        profile.bio = form.bio.data
        
        # Handle file uploads
        if form.profile_image.data:
            # Save file
            filename = secure_filename(form.profile_image.data.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            form.profile_image.data.save(filepath)
            profile.profile_image = filename
        
        db.session.add(profile)
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('lawyer.dashboard'))
    
    return render_template('lawyer/setup_profile.html', form=form)
```

#### Route 3: Update Consultation Status
```python
@lawyer_bp.route('/consultation/<int:consultation_id>/update-status', methods=['POST'])
@login_required
def update_consultation_status(consultation_id):
    consultation = Consultation.query.get_or_404(consultation_id)
    
    if consultation.lawyer_id != current_user.id:
        abort(403)
    
    new_status = request.form.get('status')
    consultation.status = new_status
    
    db.session.commit()
    
    flash(f'Consultation status updated to {new_status}', 'success')
    return redirect(url_for('lawyer.view_consultation',
                          consultation_id=consultation_id))
```

---

### 17. `app/routes/admin.py` - Admin Panel

**Purpose:** Admin dashboard, verify lawyers, manage users

**What's Inside:**

#### Route 1: Admin Dashboard
```python
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        abort(403)
    
    # Get statistics
    total_users = User.query.count()
    total_lawyers = User.query.filter_by(role='lawyer').count()
    total_customers = User.query.filter_by(role='customer').count()
    pending_verifications = LawyerProfile.query.filter_by(
        verification_status='pending'
    ).count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_lawyers=total_lawyers,
                         total_customers=total_customers,
                         pending_verifications=pending_verifications)
```

#### Route 2: Pending Lawyer Verifications
```python
@admin_bp.route('/pending-lawyers')
@login_required
def pending_lawyers():
    if current_user.role != 'admin':
        abort(403)
    
    pending_profiles = LawyerProfile.query.filter_by(
        verification_status='pending'
    ).all()
    
    return render_template('admin/pending_lawyers.html',
                         profiles=pending_profiles)
```

#### Route 3: Verify Lawyer
```python
@admin_bp.route('/verify-lawyer/<int:profile_id>', methods=['POST'])
@login_required
def verify_lawyer(profile_id):
    if current_user.role != 'admin':
        abort(403)
    
    profile = LawyerProfile.query.get_or_404(profile_id)
    action = request.form.get('action')
    
    if action == 'approve':
        profile.verification_status = 'verified'
        flash(f'Lawyer {profile.user.full_name} verified successfully!', 'success')
    elif action == 'reject':
        profile.verification_status = 'rejected'
        flash(f'Lawyer {profile.user.full_name} rejected.', 'warning')
    
    db.session.commit()
    
    return redirect(url_for('admin.pending_lawyers'))
```

#### Route 4: Manage Users
```python
@admin_bp.route('/users')
@login_required
def users():
    if current_user.role != 'admin':
        abort(403)
    
    users = User.query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html', users=users)
```

---

## 📁 TEMPLATES FOLDER (`app/templates/`)

Templates are HTML files with Jinja2 templating.

---

### 18. `app/templates/base.html` - Base Template

**Purpose:** Master template with header, footer, navigation

**What's Inside:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Law Check{% endblock %}</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom Tailwind Config -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'supreme-navy': '#1e293b',
                        'verdict-green': '#10b981',
                        'legal-pad': '#fef3c7'
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-slate-50">
    <!-- Navigation Bar -->
    <nav class="bg-supreme-navy text-white">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <a href="{{ url_for('main.index') }}" class="text-2xl font-bold">
                    ⚖️ Law Check
                </a>
                
                <!-- Navigation Links -->
                <div class="flex space-x-6">
                    <a href="{{ url_for('main.index') }}">Home</a>
                    <a href="{{ url_for('main.browse_laws') }}">Browse Laws</a>
                    <a href="{{ url_for('main.about') }}">About</a>
                    <a href="{{ url_for('main.contact') }}">Contact</a>
                    
                    {% if current_user.is_authenticated %}
                        <!-- Logged in user menu -->
                        {% if current_user.role == 'customer' %}
                            <a href="{{ url_for('customer.dashboard') }}">Dashboard</a>
                        {% elif current_user.role == 'lawyer' %}
                            <a href="{{ url_for('lawyer.dashboard') }}">Dashboard</a>
                        {% elif current_user.role == 'admin' %}
                            <a href="{{ url_for('admin.dashboard') }}">Admin</a>
                        {% endif %}
                        <a href="{{ url_for('auth.logout') }}">Logout</a>
                    {% else %}
                        <!-- Guest menu -->
                        <a href="{{ url_for('auth.login') }}">Login</a>
                        <a href="{{ url_for('auth.register') }}">Register</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </nav>
    
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <div class="max-w-7xl mx-auto px-4 mt-4">
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}
    
    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <!-- Footer -->
    <footer class="bg-supreme-navy text-white mt-12 py-8">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p>&copy; 2024 Law Check. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
```

**Key Concepts:**

**Template Inheritance:**
- Other templates extend this base
- `{% block content %}` is replaced by child content
- Header/footer appear on all pages

**Jinja2 Syntax:**
- `{{ variable }}`: Output variable
- `{% if %}`: Conditional
- `{% for %}`: Loop
- `{{ url_for('route_name') }}`: Generate URL

---

### 19. Template Organization

**Structure:**
```
templates/
├── base.html                    # Master template
├── main/                        # Public pages
│   ├── index.html               # Home page
│   ├── about.html               # About page
│   ├── contact.html             # Contact page
│   ├── browse_laws.html         # Laws browsing
│   ├── view_act.html            # Act details
│   └── view_section.html        # Section details
├── auth/                        # Authentication
│   ├── login.html               # Login page
│   └── register.html            # Registration page
├── customer/                    # Customer pages
│   ├── dashboard.html           # Customer dashboard
│   ├── browse_lawyers.html      # Browse lawyers
│   ├── book_consultation.html   # Book consultation
│   └── view_consultation.html   # Consultation details
├── lawyer/                      # Lawyer pages
│   ├── dashboard.html           # Lawyer dashboard
│   ├── setup_profile.html       # Profile setup
│   └── view_consultation.html   # Consultation details
└── admin/                       # Admin pages
    ├── dashboard.html           # Admin dashboard
    ├── pending_lawyers.html     # Verify lawyers
    └── users.html               # Manage users
```

---

## 📁 STATIC FOLDER (`app/static/`)

**Purpose:** CSS, JavaScript, images, uploads

**Structure:**
```
static/
├── css/
│   └── .gitkeep              # Placeholder for custom CSS
├── js/
│   └── .gitkeep              # Placeholder for custom JS
└── uploads/                  # User uploaded files
    ├── profile_images/
    └── documents/
```

---

## 📁 INSTANCE FOLDER (`instance/`)

**Purpose:** Instance-specific files (database, config)

**What's Inside:**
- `legal_platform.db`: SQLite database file

**Why Separate:**
- Not committed to Git
- Contains sensitive data
- Different per environment (dev, prod)

---

## 🔄 How Everything Works Together

### Request Flow Example: Booking a Consultation

1. **User clicks "Book Consultation"**
   - Browser sends GET request to `/book-consultation/5`

2. **Flask receives request**
   - Routes to `customer.book_consultation(lawyer_id=5)`

3. **Route function executes**
   ```python
   @customer_bp.route('/book-consultation/<int:lawyer_id>')
   def book_consultation(lawyer_id):
       lawyer = User.query.get_or_404(lawyer_id)  # Query database
       form = ConsultationBookingForm()           # Create form
       return render_template('customer/book_consultation.html', 
                            form=form, lawyer=lawyer)
   ```

4. **Template renders**
   - `book_consultation.html` extends `base.html`
   - Displays form with lawyer details

5. **User fills and submits form**
   - Browser sends POST request

6. **Form validation**
   ```python
   if form.validate_on_submit():
       # Create consultation
       consultation = Consultation(...)
       db.session.add(consultation)
       db.session.commit()
       flash('Booked successfully!')
       return redirect(url_for('customer.dashboard'))
   ```

7. **Database updated**
   - New row in `consultations` table

8. **User redirected**
   - Sees success message on dashboard

---

## 📊 Database Flow

### How Data is Stored and Retrieved

**Example: User Registration**

1. **User submits registration form**
2. **Form validation** (email format, password length)
3. **Check if email exists** (custom validator)
4. **Create User object**
   ```python
   user = User(
       email='john@example.com',
       full_name='John Doe',
       role='customer'
   )
   user.set_password('password123')  # Hashes password
   ```
5. **Add to database session**
   ```python
   db.session.add(user)
   ```
6. **Commit transaction**
   ```python
   db.session.commit()
   ```
7. **User saved to `users` table**

---

## 🔐 Security Features

### 1. Password Hashing
```python
# In models.py
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
```

**How it works:**
- Plain password never stored
- Uses Werkzeug's secure hashing
- One-way encryption (cannot reverse)

### 2. Login Required Decorator
```python
@customer_bp.route('/dashboard')
@login_required
def dashboard():
    # Only logged-in users can access
```

### 3. Role-Based Access Control
```python
if current_user.role != 'admin':
    abort(403)  # Forbidden
```

### 4. CSRF Protection
- All forms include CSRF token
- Prevents cross-site request forgery

---

## 🎯 Summary

### Key Files by Purpose

**Entry Point:**
- `run.py` - Starts the application

**Configuration:**
- `config.py` - Settings
- `.env` - Secrets

**Core Application:**
- `app/__init__.py` - App factory
- `app/models.py` - Database structure
- `app/forms.py` - Form validation

**Routes (Controllers):**
- `app/routes/main.py` - Public pages
- `app/routes/auth.py` - Login/Register
- `app/routes/customer.py` - Customer features
- `app/routes/lawyer.py` - Lawyer features
- `app/routes/admin.py` - Admin panel

**Views (Templates):**
- `app/templates/base.html` - Master template
- `app/templates/*/` - Page-specific templates

**Utilities:**
- `create_admin.py` - Create admin user
- `seed_laws.py` - Populate laws database
- `setup.bat` - Automated setup

---

## 💡 Quick Reference

**To start the app:**
```bash
python run.py
```

**To create admin:**
```bash
python create_admin.py
```

**To seed laws:**
```bash
python seed_laws.py
```

**To access:**
- Home: http://127.0.0.1:5000
- Login: http://127.0.0.1:5000/login
- Admin: http://127.0.0.1:5000/admin/dashboard

---

This documentation covers every major file in your project! Let me know if you need clarification on any specific file or concept. 🚀
