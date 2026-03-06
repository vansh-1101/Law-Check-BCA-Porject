"""
Customer routes - Dashboard, Browse Lawyers, Book Consultation
"""
import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, LawyerProfile, Consultation, Message
from datetime import datetime, timedelta

customer_bp = Blueprint('customer', __name__, url_prefix='/customer')

VALID_CATEGORIES = ['civil', 'criminal', 'corporate', 'family', 'property',
                    'labor', 'cyber', 'constitutional', 'tax', 'consumer', 'ip', 'other']


def customer_required(f):
    """Decorator to require customer role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'customer':
            flash('Access denied. Customer account required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@customer_bp.route('/dashboard')
@login_required
@customer_required
def dashboard():
    """Customer dashboard"""
    consultations = Consultation.query.filter_by(customer_id=current_user.id)\
        .order_by(Consultation.created_at.desc())\
        .all()

    total_consultations = len(consultations)
    pending_consultations = len([c for c in consultations if c.status == 'pending'])
    completed_consultations = len([c for c in consultations if c.status == 'completed'])

    return render_template('customer/dashboard.html',
                         title='Dashboard',
                         consultations=consultations,
                         total_consultations=total_consultations,
                         pending_consultations=pending_consultations,
                         completed_consultations=completed_consultations)


@customer_bp.route('/browse-lawyers')
@login_required
@customer_required
def browse_lawyers():
    """Browse verified lawyers"""
    specialization = request.args.get('specialization', '')
    min_fee = request.args.get('min_fee', type=float)
    max_fee = request.args.get('max_fee', type=float)
    min_experience = request.args.get('min_experience', type=int)

    query = db.session.query(User, LawyerProfile)\
        .join(LawyerProfile, User.id == LawyerProfile.user_id)\
        .filter(LawyerProfile.verification_status == 'verified')

    if specialization:
        query = query.filter(LawyerProfile.specializations.contains(specialization))
    if min_fee is not None:
        query = query.filter(LawyerProfile.consultation_fee >= min_fee)
    if max_fee is not None:
        query = query.filter(LawyerProfile.consultation_fee <= max_fee)
    if min_experience is not None:
        query = query.filter(LawyerProfile.experience_years >= min_experience)

    lawyers = query.all()

    return render_template('customer/browse_lawyers.html',
                         title='Browse Lawyers',
                         lawyers=lawyers,
                         specialization=specialization)


@customer_bp.route('/book-consultation/<int:lawyer_id>', methods=['GET', 'POST'])
@login_required
@customer_required
def book_consultation(lawyer_id):
    """Book consultation with a lawyer — plain form, no WTForms"""
    lawyer = User.query.get_or_404(lawyer_id)

    if lawyer.role != 'lawyer':
        flash('Invalid lawyer selected.', 'danger')
        return redirect(url_for('customer.browse_lawyers'))

    # Get lawyer profile for display
    lawyer_profile = LawyerProfile.query.filter_by(user_id=lawyer.id).first()
    specializations = []
    if lawyer_profile and lawyer_profile.specializations:
        try:
            specializations = json.loads(lawyer_profile.specializations)
        except:
            specializations = [lawyer_profile.specializations]

    # Minimum datetime = now + 1 hour
    min_date = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')

    errors = {}
    consultation_date = ''
    category = ''
    issue_description = ''

    if request.method == 'POST':
        consultation_date = request.form.get('consultation_date', '').strip()
        category          = request.form.get('category', '').strip()
        issue_description = request.form.get('issue_description', '').strip()

        # Validate date
        if not consultation_date:
            errors['consultation_date'] = 'Please select a date and time.'
        else:
            try:
                parsed_date = datetime.strptime(consultation_date, '%Y-%m-%dT%H:%M')
                if parsed_date <= datetime.now():
                    errors['consultation_date'] = 'Please select a future date and time.'
            except ValueError:
                errors['consultation_date'] = 'Invalid date format.'

        # Validate category
        if not category or category not in VALID_CATEGORIES:
            errors['category'] = 'Please select a valid category.'

        # Validate description
        if not issue_description:
            errors['issue_description'] = 'Please describe your issue.'
        elif len(issue_description) < 20:
            errors['issue_description'] = 'Description must be at least 20 characters.'
        elif len(issue_description) > 1000:
            errors['issue_description'] = 'Description must not exceed 1000 characters.'

        # If no errors, create consultation
        if not errors:
            consultation = Consultation(
                customer_id=current_user.id,
                lawyer_id=lawyer_id,
                consultation_date=parsed_date,
                category=category,
                issue_description=issue_description,
                status='pending'
            )
            db.session.add(consultation)
            db.session.commit()
            flash('Consultation booked successfully! The lawyer will confirm shortly.', 'success')
            return redirect(url_for('customer.dashboard'))

    return render_template('customer/book_consultation.html',
                         title='Book Consultation',
                         lawyer=lawyer,
                         lawyer_profile=lawyer_profile,
                         specializations=specializations,
                         min_date=min_date,
                         errors=errors,
                         consultation_date=consultation_date,
                         category=category,
                         issue_description=issue_description)


@customer_bp.route('/consultation/<int:consultation_id>')
@login_required
@customer_required
def view_consultation(consultation_id):
    """View consultation details"""
    consultation = Consultation.query.get_or_404(consultation_id)

    if consultation.customer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.dashboard'))

    messages = Message.query.filter_by(consultation_id=consultation_id)\
        .order_by(Message.created_at.asc())\
        .all()

    return render_template('customer/view_consultation.html',
                         title='Consultation Details',
                         consultation=consultation,
                         messages=messages)


@customer_bp.route('/consultation/<int:consultation_id>/send-message', methods=['POST'])
@login_required
@customer_required
def send_message(consultation_id):
    """Send message in consultation"""
    consultation = Consultation.query.get_or_404(consultation_id)

    if consultation.customer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.dashboard'))

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

    return redirect(url_for('customer.view_consultation', consultation_id=consultation_id))

