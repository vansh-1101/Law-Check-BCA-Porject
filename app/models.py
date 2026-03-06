"""
Database models for Legal Consultation Platform
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model for customers, lawyers, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), nullable=False)  # 'customer', 'lawyer', 'admin'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lawyer_profile = db.relationship('LawyerProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    customer_consultations = db.relationship('Consultation', foreign_keys='Consultation.customer_id', backref='customer', lazy='dynamic')
    lawyer_consultations = db.relationship('Consultation', foreign_keys='Consultation.lawyer_id', backref='lawyer', lazy='dynamic')
    messages = db.relationship('Message', backref='sender', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class LawyerProfile(db.Model):
    """Extended profile for lawyers"""
    __tablename__ = 'lawyer_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    bar_council_id = db.Column(db.String(50), unique=True, nullable=False)
    specializations = db.Column(db.Text)  # JSON string of specializations
    experience_years = db.Column(db.Integer)
    education = db.Column(db.Text)
    languages = db.Column(db.Text)  # JSON string of languages
    consultation_fee = db.Column(db.Float)
    verification_status = db.Column(db.String(20), default='pending')  # 'pending', 'verified', 'rejected'
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    credentials_document = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LawyerProfile {self.bar_council_id}>'


class Consultation(db.Model):
    """Consultation booking model"""
    __tablename__ = 'consultations'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lawyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    consultation_date = db.Column(db.DateTime, nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # 'civil', 'criminal', 'corporate', etc.
    status = db.Column(db.String(20), default='pending')  # 'pending', 'confirmed', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    messages = db.relationship('Message', backref='consultation', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Consultation {self.id} - {self.status}>'


class Message(db.Model):
    """Message model for consultation chat"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    consultation_id = db.Column(db.Integer, db.ForeignKey('consultations.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Message {self.id}>'


class LegalAct(db.Model):
    """Model for Indian Legal Acts"""
    __tablename__ = 'legal_acts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Full name of the act
    short_name = db.Column(db.String(50), nullable=False)  # Abbreviated name (e.g., "IPC")
    year = db.Column(db.Integer, nullable=False)  # Year of enactment
    category = db.Column(db.String(50), nullable=False)  # Criminal, Civil, Constitutional, etc.
    description = db.Column(db.Text)  # Brief description of the act
    total_sections = db.Column(db.Integer, default=0)  # Total number of sections
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sections = db.relationship('LegalSection', backref='act', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<LegalAct {self.short_name}, {self.year}>'



class LegalSection(db.Model):
    """Model for sections within Legal Acts"""
    __tablename__ = 'legal_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    act_id = db.Column(db.Integer, db.ForeignKey('legal_acts.id'), nullable=False)
    section_number = db.Column(db.String(20), nullable=False)  # e.g., "302", "498A"
    title = db.Column(db.String(500), nullable=False)  # Section title/heading
    description = db.Column(db.Text, nullable=False)  # Full section text
    keywords = db.Column(db.Text)  # Comma-separated keywords for search
    
    # Legal Problem Analyzer fields
    penalty = db.Column(db.Text)  # Punishment details (e.g., "Up to 3 years imprisonment and fine")
    is_bailable = db.Column(db.Boolean, default=True)  # Whether offense is bailable
    is_cognizable = db.Column(db.Boolean, default=False)  # Whether police can arrest without warrant
    is_compoundable = db.Column(db.Boolean, default=False)  # Whether can be settled out of court
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LegalSection {self.section_number}>'


class ContactMessage(db.Model):
    """Contact form submissions"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.id} - {self.subject}>'

