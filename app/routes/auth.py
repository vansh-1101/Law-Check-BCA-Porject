"""
Authentication routes - Login, Register, Logout
All validation is done manually with strict checks.
"""
import re
import json
import secrets
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User, LawyerProfile, LawyerPayment

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Strict email regex - rejects phone numbers, random text etc.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

# Phone regex - 10 digits, optionally prefixed with +91 or 0
PHONE_REGEX = re.compile(r'^(\+91[\-\s]?)?[0]?[6789]\d{9}$')

SPECIALIZATION_CHOICES = [
    'Criminal Law', 'Civil Law', 'Family Law', 'Divorce Law',
    'Corporate Law', 'Tax Law', 'Property Law', 'Labor Law',
    'Consumer Law', 'Cyber Law', 'Constitutional Law', 'PIL',
    'Intellectual Property', 'IT Law', 'NDPS Law', 'Banking Law',
    'Environmental Law', 'Immigration Law', 'Human Rights', 'Other'
]


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with strict validation"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    errors = {}

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email     = request.form.get('email', '').strip().lower()
        phone     = request.form.get('phone', '').strip()
        role      = request.form.get('role', '').strip()
        password  = request.form.get('password', '')
        confirm   = request.form.get('confirm_password', '')

        # Lawyer-specific fields
        bar_council_id = request.form.get('bar_council_id', '').strip()
        practice_areas = request.form.getlist('practice_areas')
        experience_years = request.form.get('experience_years', '').strip()
        city = request.form.get('city', '').strip()
        state = request.form.get('state', '').strip()

        # --- Validate common fields ---
        if not full_name or len(full_name) < 2:
            errors['full_name'] = 'Full name is required (minimum 2 characters).'

        if not email:
            errors['email'] = 'Email is required.'
        elif not EMAIL_REGEX.match(email):
            errors['email'] = 'Enter a valid email address (e.g. user@gmail.com).'
        else:
            existing = User.query.filter_by(email=email).first()
            if existing:
                errors['email'] = 'This email is already registered. Please login.'

        if phone:
            clean_phone = phone.replace(' ', '').replace('-', '')
            if not PHONE_REGEX.match(clean_phone):
                errors['phone'] = 'Enter a valid 10-digit Indian phone number.'

        if role not in ('customer', 'lawyer'):
            errors['role'] = 'Please select Customer or Lawyer.'

        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters.'

        if password != confirm:
            errors['confirm_password'] = 'Passwords do not match.'

        # --- Validate lawyer-specific fields ---
        if role == 'lawyer':
            if not bar_council_id or len(bar_council_id) < 3:
                errors['bar_council_id'] = 'Bar Council ID is required (min 3 characters).'
            else:
                # Check for duplicate bar council ID
                existing_lawyer = LawyerProfile.query.filter_by(bar_council_id=bar_council_id).first()
                if existing_lawyer:
                    errors['bar_council_id'] = 'This Bar Council ID is already registered. Please use a different one or contact support.'
            if not practice_areas:
                errors['practice_areas'] = 'Select at least one practice area.'
            if experience_years:
                try:
                    exp = int(experience_years)
                    if exp < 0 or exp > 60:
                        errors['experience_years'] = 'Experience must be 0-60 years.'
                except ValueError:
                    errors['experience_years'] = 'Enter a valid number.'

        # --- If no errors, create user ---
        if not errors:
            try:
                user = User(
                    email=email,
                    full_name=full_name,
                    phone=phone,
                    role=role
                )
                user.set_password(password)
                db.session.add(user)
                db.session.flush()  # Get user.id before creating profile

                # Create lawyer profile if role is lawyer
                if role == 'lawyer':
                    lawyer_profile = LawyerProfile(
                        user_id=user.id,
                        bar_council_id=bar_council_id,
                        specializations=json.dumps(practice_areas),
                        experience_years=int(experience_years) if experience_years else 0,
                        verification_status='pending'
                    )
                    db.session.add(lawyer_profile)

                db.session.commit()

                # For lawyers: create a pending payment and redirect to payment page
                if role == 'lawyer':
                    payment_token = secrets.token_hex(32)
                    payment = LawyerPayment(
                        user_id=user.id,
                        amount=2.0,
                        payment_type='membership',
                        status='pending',
                        order_token=payment_token
                    )
                    db.session.add(payment)
                    db.session.commit()
                    session['lawyer_payment_token'] = payment_token
                    flash('Account created! Please complete the ₹2 membership payment to activate your account.', 'info')
                    return redirect(url_for('auth.lawyer_payment'))

                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('auth.login'))

            except Exception:
                db.session.rollback()
                errors['general'] = 'Registration failed due to a server error. Please try again.'

    else:
        full_name = email = phone = role = ''
        bar_council_id = ''
        practice_areas = []
        experience_years = ''
        city = ''
        state = ''

    return render_template('auth/register.html',
                           title='Register',
                           errors=errors,
                           full_name=full_name,
                           email=email,
                           phone=phone,
                           role=role,
                           bar_council_id=bar_council_id,
                           practice_areas=practice_areas,
                           experience_years=experience_years,
                           city=city,
                           state=state,
                           specialization_choices=SPECIALIZATION_CHOICES)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login with strict validation"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    error = None

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '').strip()

        # 1. Both fields required
        if not email or not password:
            error = 'Please enter both email and password.'

        # 2. Must be a valid email — rejects phone numbers, random text
        elif not EMAIL_REGEX.match(email):
            error = 'Please enter a valid email address (e.g. user@gmail.com). Phone numbers are not allowed.'

        # 3. Password minimum length
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'

        else:
            # 4. Check credentials in database
            user = User.query.filter_by(email=email).first()

            if user is None or not user.check_password(password):
                error = 'Invalid email or password. Please try again.'
            elif not user.is_active:
                error = 'Your account has been deactivated. Contact support.'
            else:
                # Login successful
                login_user(user, remember=True)
                flash(f'Welcome back, {user.full_name}!', 'success')

                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)

                if user.role == 'customer':
                    return redirect(url_for('customer.dashboard'))
                elif user.role == 'lawyer':
                    return redirect(url_for('lawyer.dashboard'))
                elif user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                else:
                    return redirect(url_for('main.index'))

    return render_template('auth/login.html', error=error, title='Login')


@auth_bp.route('/logout')
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.index'))


# ─────────────────────────────────────────────────────────────────────────────
# RAZORPAY PAYMENT — Lawyer Membership (₹2)
# ─────────────────────────────────────────────────────────────────────────────

@auth_bp.route('/lawyer-payment', methods=['GET', 'POST'])
def lawyer_payment():
    """Secure lawyer membership payment page (₹2 fixed fee) — Manual Verification"""
    # Get order token from session — prevents accessing page without registering
    token = session.get('lawyer_payment_token')
    if not token:
        flash('Invalid payment session. Please register first.', 'danger')
        return redirect(url_for('auth.register'))

    payment = LawyerPayment.query.filter_by(order_token=token).first()
    if not payment:
        flash('Payment session expired or invalid. Please register again.', 'danger')
        return redirect(url_for('auth.register'))

    if payment.status in ['processing', 'completed']:
        flash('Payment already submitted and is currently in process. You will be notified once verified.', 'info')
        # They can safely log in, the system will just show them their profile is pending
        return redirect(url_for('auth.login'))

    errors = {}

    if request.method == 'POST':
        payment_type = request.form.get('payment_type', 'membership').strip()
        payment_method = request.form.get('payment_method', 'card').strip()

        if payment_method == 'qr':
            # ── QR / UPI payment validation ──
            upi_txn_id   = request.form.get('upi_transaction_id', '').strip()
            upi_payer    = request.form.get('upi_payer_name', '').strip()

            if not upi_txn_id or len(upi_txn_id) < 4:
                errors['upi_transaction_id'] = 'Enter a valid UPI transaction ID or UTR number (min 4 characters).'
            if not upi_payer or len(upi_payer) < 2:
                errors['upi_payer_name'] = 'Enter your name as shown in your UPI app.'

            if not errors:
                payment.payment_method = 'qr'
                payment.payment_type   = payment_type
                payment.transaction_id = upi_txn_id
                payment.card_last4     = None
                payment.status = 'processing'  # Needs admin approval
                db.session.commit()
                session.pop('lawyer_payment_token', None)
                flash('✅ UPI payment details submitted! Our admins will verify the transaction and activate your account shortly.', 'success')
                return redirect(url_for('auth.login'))

        else:
            # ── Card payment validation ──
            card_number  = request.form.get('card_number', '').replace(' ', '').strip()
            card_name    = request.form.get('card_name', '').strip()
            card_expiry  = request.form.get('card_expiry', '').strip()
            card_cvv     = request.form.get('card_cvv', '').strip()

            if not card_number or not card_number.isdigit() or len(card_number) not in (15, 16):
                errors['card_number'] = 'Enter a valid 15 or 16-digit card number.'
            if not card_name or len(card_name) < 2:
                errors['card_name'] = 'Enter the cardholder name as on card.'
            if not card_expiry or len(card_expiry) != 5 or card_expiry[2] != '/':
                errors['card_expiry'] = 'Enter expiry in MM/YY format.'
            if not card_cvv or not card_cvv.isdigit() or len(card_cvv) not in (3, 4):
                errors['card_cvv'] = 'Enter a valid 3 or 4-digit CVV.'

            if not errors:
                payment.payment_method = 'card'
                payment.payment_type   = payment_type
                payment.card_last4     = card_number[-4:]
                payment.transaction_id = 'CARD-' + secrets.token_hex(10).upper()
                payment.status = 'processing'  # Needs admin approval
                db.session.commit()
                session.pop('lawyer_payment_token', None)
                flash('✅ Payment details submitted! Your payment is currently in process. Our admins will verify the transaction and update your account status shortly.', 'success')
                return redirect(url_for('auth.login'))

    user = User.query.get(payment.user_id)
    return render_template('auth/lawyer_payment.html',
                           title='Membership Payment',
                           payment=payment,
                           user=user,
                           errors=errors)

