"""
Lawyer routes - Dashboard, Profile Setup, Manage Consultations
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import json
from app import db
from app.models import User, LawyerProfile, Consultation, Message

lawyer_bp = Blueprint('lawyer', __name__, url_prefix='/lawyer')

SPECIALIZATION_CHOICES = [
    'Criminal Law', 'Civil Law', 'Family Law', 'Divorce Law',
    'Corporate Law', 'Tax Law', 'Property Law', 'Labor Law',
    'Consumer Law', 'Cyber Law', 'Constitutional Law', 'PIL',
    'Intellectual Property', 'IT Law', 'NDPS Law', 'Banking Law',
    'Environmental Law', 'Immigration Law', 'Human Rights', 'Other'
]


def lawyer_required(f):
    """Decorator to require lawyer role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'lawyer':
            flash('Access denied. Lawyer account required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@lawyer_bp.route('/dashboard')
@login_required
@lawyer_required
def dashboard():
    """Lawyer dashboard"""
    consultations = Consultation.query.filter_by(lawyer_id=current_user.id)\
        .order_by(Consultation.created_at.desc())\
        .all()

    profile = LawyerProfile.query.filter_by(user_id=current_user.id).first()

    total_consultations = len(consultations)
    pending_consultations = len([c for c in consultations if c.status == 'pending'])
    completed_consultations = len([c for c in consultations if c.status == 'completed'])

    return render_template('lawyer/dashboard.html',
                         title='Dashboard',
                         profile=profile,
                         consultations=consultations,
                         total_consultations=total_consultations,
                         pending_consultations=pending_consultations,
                         completed_consultations=completed_consultations)


@lawyer_bp.route('/profile/setup', methods=['GET', 'POST'])
@login_required
@lawyer_required
def setup_profile():
    """Setup or edit lawyer profile — plain form, no WTForms"""
    profile = LawyerProfile.query.filter_by(user_id=current_user.id).first()

    errors = {}

    if request.method == 'POST':
        bar_council_id = request.form.get('bar_council_id', '').strip()
        specializations_list = request.form.getlist('specializations')
        experience_years = request.form.get('experience_years', '').strip()
        education = request.form.get('education', '').strip()
        languages_raw = request.form.get('languages', '').strip()
        consultation_fee = request.form.get('consultation_fee', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()

        # --- Validation ---
        if not bar_council_id or len(bar_council_id) < 3:
            errors['bar_council_id'] = 'Bar Council ID is required (min 3 characters).'

        if not specializations_list:
            errors['specializations'] = 'Select at least one specialization.'

        if not experience_years:
            errors['experience_years'] = 'Years of experience is required.'
        else:
            try:
                experience_years = int(experience_years)
                if experience_years < 0 or experience_years > 60:
                    errors['experience_years'] = 'Experience must be between 0 and 60 years.'
            except ValueError:
                errors['experience_years'] = 'Enter a valid number.'

        if not education:
            errors['education'] = 'Education details are required.'

        if not consultation_fee:
            errors['consultation_fee'] = 'Consultation fee is required.'
        else:
            try:
                consultation_fee = float(consultation_fee)
                if consultation_fee < 0:
                    errors['consultation_fee'] = 'Fee cannot be negative.'
            except ValueError:
                errors['consultation_fee'] = 'Enter a valid amount.'

        languages = [l.strip() for l in languages_raw.split(',') if l.strip()] if languages_raw else []

        # Handle file uploads
        profile_image_filename = None
        credentials_filename = None

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename and allowed_file(file.filename, {'jpg', 'jpeg', 'png'}):
                filename = secure_filename(file.filename)
                profile_image_filename = f"profile_{current_user.id}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], profile_image_filename))

        if 'credentials_document' in request.files:
            file = request.files['credentials_document']
            if file and file.filename and allowed_file(file.filename, {'pdf', 'doc', 'docx'}):
                filename = secure_filename(file.filename)
                credentials_filename = f"credentials_{current_user.id}_{filename}"
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], credentials_filename))

        if not errors:
            if profile:
                # Update existing
                profile.bar_council_id = bar_council_id
                profile.specializations = json.dumps(specializations_list)
                profile.experience_years = experience_years
                profile.education = education
                profile.languages = json.dumps(languages)
                profile.consultation_fee = consultation_fee
                profile.bio = bio
                if profile_image_filename:
                    profile.profile_image = profile_image_filename
                if credentials_filename:
                    profile.credentials_document = credentials_filename
            else:
                # Create new
                profile = LawyerProfile(
                    user_id=current_user.id,
                    bar_council_id=bar_council_id,
                    specializations=json.dumps(specializations_list),
                    experience_years=experience_years,
                    education=education,
                    languages=json.dumps(languages),
                    consultation_fee=consultation_fee,
                    bio=bio,
                    profile_image=profile_image_filename,
                    credentials_document=credentials_filename,
                    verification_status='pending'
                )
                db.session.add(profile)

            db.session.commit()
            flash('Profile saved successfully! Awaiting admin verification.', 'success')
            return redirect(url_for('lawyer.dashboard'))

    # Pre-fill values for GET or validation failure
    if profile and request.method == 'GET':
        prefill = {
            'bar_council_id': profile.bar_council_id or '',
            'specializations': json.loads(profile.specializations) if profile.specializations else [],
            'experience_years': profile.experience_years or '',
            'education': profile.education or '',
            'languages': ', '.join(json.loads(profile.languages)) if profile.languages else '',
            'consultation_fee': profile.consultation_fee or '',
            'bio': profile.bio or '',
            'city': '',
            'state': '',
        }
    elif request.method == 'POST':
        prefill = {
            'bar_council_id': request.form.get('bar_council_id', ''),
            'specializations': request.form.getlist('specializations'),
            'experience_years': request.form.get('experience_years', ''),
            'education': request.form.get('education', ''),
            'languages': request.form.get('languages', ''),
            'consultation_fee': request.form.get('consultation_fee', ''),
            'bio': request.form.get('bio', ''),
            'city': request.form.get('city', ''),
            'state': request.form.get('state', ''),
        }
    else:
        prefill = {}

    return render_template('lawyer/setup_profile.html',
                         title='Setup Profile',
                         profile=profile,
                         prefill=prefill,
                         errors=errors,
                         specialization_choices=SPECIALIZATION_CHOICES)


@lawyer_bp.route('/consultation/<int:consultation_id>')
@login_required
@lawyer_required
def view_consultation(consultation_id):
    """View consultation details"""
    consultation = Consultation.query.get_or_404(consultation_id)

    if consultation.lawyer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('lawyer.dashboard'))

    messages = Message.query.filter_by(consultation_id=consultation_id)\
        .order_by(Message.created_at.asc())\
        .all()

    return render_template('lawyer/view_consultation.html',
                         title='Consultation Details',
                         consultation=consultation,
                         messages=messages)


@lawyer_bp.route('/consultation/<int:consultation_id>/update-status/<status>')
@login_required
@lawyer_required
def update_consultation_status(consultation_id, status):
    """Update consultation status"""
    consultation = Consultation.query.get_or_404(consultation_id)

    if consultation.lawyer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('lawyer.dashboard'))

    if status in ['confirmed', 'completed', 'cancelled']:
        consultation.status = status
        db.session.commit()
        flash(f'Consultation status updated to {status}.', 'success')

    return redirect(url_for('lawyer.view_consultation', consultation_id=consultation_id))


@lawyer_bp.route('/consultation/<int:consultation_id>/send-message', methods=['POST'])
@login_required
@lawyer_required
def send_message(consultation_id):
    """Send message in consultation — plain form"""
    consultation = Consultation.query.get_or_404(consultation_id)

    if consultation.lawyer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('lawyer.dashboard'))

    msg_text = request.form.get('message', '').strip()
    if msg_text and len(msg_text) <= 1000:
        message = Message(
            consultation_id=consultation_id,
            sender_id=current_user.id,
            message=msg_text
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully.', 'success')
    else:
        flash('Message cannot be empty or exceed 1000 characters.', 'danger')

    return redirect(url_for('lawyer.view_consultation', consultation_id=consultation_id))
