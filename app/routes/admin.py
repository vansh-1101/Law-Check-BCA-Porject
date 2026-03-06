"""
Admin routes - Dashboard, Verify Lawyers, Manage Users, Manage Laws
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, LawyerProfile, Consultation, LegalAct, LegalSection, ContactMessage

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin account required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    total_lawyers = User.query.filter_by(role='lawyer').count()
    total_consultations = Consultation.query.count()
    total_acts = LegalAct.query.count()
    total_sections = LegalSection.query.count()
    total_messages = ContactMessage.query.count()

    pending_lawyers = db.session.query(User, LawyerProfile)\
        .join(LawyerProfile, User.id == LawyerProfile.user_id)\
        .filter(LawyerProfile.verification_status == 'pending')\
        .all()

    recent_consultations = Consultation.query\
        .order_by(Consultation.created_at.desc())\
        .limit(10)\
        .all()

    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_customers=total_customers,
                         total_lawyers=total_lawyers,
                         total_consultations=total_consultations,
                         total_acts=total_acts,
                         total_sections=total_sections,
                         total_messages=total_messages,
                         pending_lawyers=pending_lawyers,
                         recent_consultations=recent_consultations)


@admin_bp.route('/lawyers/pending')
@login_required
@admin_required
def pending_lawyers():
    """View pending lawyer verifications"""
    lawyers = db.session.query(User, LawyerProfile)\
        .join(LawyerProfile, User.id == LawyerProfile.user_id)\
        .filter(LawyerProfile.verification_status == 'pending')\
        .all()

    return render_template('admin/pending_lawyers.html',
                         title='Pending Verifications',
                         lawyers=lawyers)


@admin_bp.route('/lawyer/<int:lawyer_id>/verify')
@login_required
@admin_required
def verify_lawyer(lawyer_id):
    """Verify a lawyer"""
    profile = LawyerProfile.query.filter_by(user_id=lawyer_id).first_or_404()
    profile.verification_status = 'verified'
    db.session.commit()

    flash('Lawyer verified successfully!', 'success')
    return redirect(url_for('admin.pending_lawyers'))


@admin_bp.route('/lawyer/<int:lawyer_id>/reject')
@login_required
@admin_required
def reject_lawyer(lawyer_id):
    """Reject a lawyer"""
    profile = LawyerProfile.query.filter_by(user_id=lawyer_id).first_or_404()
    profile.verification_status = 'rejected'
    db.session.commit()

    flash('Lawyer verification rejected.', 'warning')
    return redirect(url_for('admin.pending_lawyers'))


@admin_bp.route('/users')
@login_required
@admin_required
def manage_users():
    """Manage all users"""
    users = User.query.order_by(User.created_at.desc()).all()

    return render_template('admin/manage_users.html',
                         title='Manage Users',
                         users=users)


@admin_bp.route('/user/<int:user_id>/toggle-active')
@login_required
@admin_required
def toggle_user_active(user_id):
    """Toggle user active status"""
    user = User.query.get_or_404(user_id)

    if user.role == 'admin':
        flash('Cannot deactivate admin users.', 'danger')
        return redirect(url_for('admin.manage_users'))

    user.is_active = not user.is_active
    db.session.commit()

    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {status} successfully.', 'success')

    return redirect(url_for('admin.manage_users'))


# ========== LAWS MANAGEMENT ==========

@admin_bp.route('/laws')
@login_required
@admin_required
def manage_laws():
    """List all acts and sections for management"""
    acts = LegalAct.query.order_by(LegalAct.name).all()
    return render_template('admin/manage_laws.html', title='Manage Laws', acts=acts)


@admin_bp.route('/laws/add-act', methods=['GET', 'POST'])
@login_required
@admin_required
def add_act():
    """Add a new legal act"""
    errors = {}
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        short_name = request.form.get('short_name', '').strip()
        year = request.form.get('year', '').strip()
        category = request.form.get('category', '').strip()
        description = request.form.get('description', '').strip()

        if not name: errors['name'] = 'Act name is required.'
        if not short_name: errors['short_name'] = 'Short name is required.'
        if not year:
            errors['year'] = 'Year is required.'
        else:
            try:
                year = int(year)
                if year < 1800 or year > 2030:
                    errors['year'] = 'Year must be between 1800 and 2030.'
            except ValueError:
                errors['year'] = 'Enter a valid year.'
        if not category: errors['category'] = 'Category is required.'

        if not errors:
            act = LegalAct(name=name, short_name=short_name, year=year,
                          category=category, description=description)
            db.session.add(act)
            db.session.commit()
            flash(f'Act "{name}" added successfully!', 'success')
            return redirect(url_for('admin.manage_laws'))

    return render_template('admin/edit_act.html', title='Add Act',
                         act=None, errors=errors)


@admin_bp.route('/laws/edit-act/<int:act_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_act(act_id):
    """Edit an existing legal act"""
    act = LegalAct.query.get_or_404(act_id)
    errors = {}

    if request.method == 'POST':
        act.name = request.form.get('name', '').strip()
        act.short_name = request.form.get('short_name', '').strip()
        year_val = request.form.get('year', '').strip()
        act.category = request.form.get('category', '').strip()
        act.description = request.form.get('description', '').strip()

        if not act.name: errors['name'] = 'Act name is required.'
        if not act.short_name: errors['short_name'] = 'Short name is required.'
        try:
            act.year = int(year_val)
        except (ValueError, TypeError):
            errors['year'] = 'Enter a valid year.'
        if not act.category: errors['category'] = 'Category is required.'

        if not errors:
            db.session.commit()
            flash(f'Act "{act.name}" updated successfully!', 'success')
            return redirect(url_for('admin.manage_laws'))

    return render_template('admin/edit_act.html', title='Edit Act',
                         act=act, errors=errors)


@admin_bp.route('/laws/delete-act/<int:act_id>', methods=['POST'])
@login_required
@admin_required
def delete_act(act_id):
    """Delete a legal act and all its sections"""
    act = LegalAct.query.get_or_404(act_id)
    name = act.name
    db.session.delete(act)
    db.session.commit()
    flash(f'Act "{name}" and all its sections deleted.', 'warning')
    return redirect(url_for('admin.manage_laws'))


@admin_bp.route('/laws/act/<int:act_id>/add-section', methods=['GET', 'POST'])
@login_required
@admin_required
def add_section(act_id):
    """Add a section to an act"""
    act = LegalAct.query.get_or_404(act_id)
    errors = {}

    if request.method == 'POST':
        section_number = request.form.get('section_number', '').strip()
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        keywords = request.form.get('keywords', '').strip()
        penalty = request.form.get('penalty', '').strip()
        is_bailable = request.form.get('is_bailable') == 'on'
        is_cognizable = request.form.get('is_cognizable') == 'on'
        is_compoundable = request.form.get('is_compoundable') == 'on'

        if not section_number: errors['section_number'] = 'Section number is required.'
        if not title: errors['title'] = 'Title is required.'
        if not description: errors['description'] = 'Description is required.'

        if not errors:
            section = LegalSection(
                act_id=act.id,
                section_number=section_number,
                title=title,
                description=description,
                keywords=keywords,
                penalty=penalty,
                is_bailable=is_bailable,
                is_cognizable=is_cognizable,
                is_compoundable=is_compoundable
            )
            db.session.add(section)
            act.total_sections = LegalSection.query.filter_by(act_id=act.id).count() + 1
            db.session.commit()
            flash(f'Section {section_number} added successfully!', 'success')
            return redirect(url_for('admin.manage_laws'))

    return render_template('admin/edit_section.html', title='Add Section',
                         act=act, section=None, errors=errors)


@admin_bp.route('/laws/edit-section/<int:section_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_section(section_id):
    """Edit an existing section"""
    section = LegalSection.query.get_or_404(section_id)
    act = section.act
    errors = {}

    if request.method == 'POST':
        section.section_number = request.form.get('section_number', '').strip()
        section.title = request.form.get('title', '').strip()
        section.description = request.form.get('description', '').strip()
        section.keywords = request.form.get('keywords', '').strip()
        section.penalty = request.form.get('penalty', '').strip()
        section.is_bailable = request.form.get('is_bailable') == 'on'
        section.is_cognizable = request.form.get('is_cognizable') == 'on'
        section.is_compoundable = request.form.get('is_compoundable') == 'on'

        if not section.section_number: errors['section_number'] = 'Section number is required.'
        if not section.title: errors['title'] = 'Title is required.'
        if not section.description: errors['description'] = 'Description is required.'

        if not errors:
            db.session.commit()
            flash(f'Section {section.section_number} updated!', 'success')
            return redirect(url_for('admin.manage_laws'))

    return render_template('admin/edit_section.html', title='Edit Section',
                         act=act, section=section, errors=errors)


@admin_bp.route('/laws/delete-section/<int:section_id>', methods=['POST'])
@login_required
@admin_required
def delete_section(section_id):
    """Delete a section"""
    section = LegalSection.query.get_or_404(section_id)
    act = section.act
    num = section.section_number
    db.session.delete(section)
    act.total_sections = max(0, LegalSection.query.filter_by(act_id=act.id).count() - 1)
    db.session.commit()
    flash(f'Section {num} deleted.', 'warning')
    return redirect(url_for('admin.manage_laws'))

