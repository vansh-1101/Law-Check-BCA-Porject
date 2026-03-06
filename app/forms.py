"""
WTForms for form validation
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User


class RegistrationForm(FlaskForm):
    """User registration form"""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register as', choices=[('customer', 'Customer'), ('lawyer', 'Lawyer')], validators=[DataRequired()])
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class LawyerProfileForm(FlaskForm):
    """Lawyer profile setup form"""
    bar_council_id = StringField('Bar Council ID', validators=[DataRequired(), Length(max=50)])
    specializations = StringField('Specializations (comma-separated)', validators=[DataRequired()])
    experience_years = IntegerField('Years of Experience', validators=[DataRequired()])
    education = TextAreaField('Education', validators=[DataRequired()])
    languages = StringField('Languages (comma-separated)', validators=[DataRequired()])
    consultation_fee = FloatField('Consultation Fee (₹)', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    profile_image = FileField('Profile Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    credentials_document = FileField('Credentials Document', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])


class ConsultationBookingForm(FlaskForm):
    """Consultation booking form"""
    lawyer_id = SelectField('Select Lawyer', coerce=int, validators=[DataRequired()])
    consultation_date = DateTimeField('Consultation Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('civil', 'Civil Law'),
        ('criminal', 'Criminal Law'),
        ('corporate', 'Corporate Law'),
        ('family', 'Family Law'),
        ('property', 'Property Law'),
        ('labor', 'Labor Law'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    issue_description = TextAreaField('Describe Your Issue', validators=[DataRequired(), Length(min=20, max=1000)])


class MessageForm(FlaskForm):
    """Message form for consultation chat"""
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=1, max=1000)])
