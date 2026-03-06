"""
Main routes - Landing page, About, Contact
"""
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import re
from app import db
from app.models import User, LawyerProfile, LegalAct, LegalSection, ContactMessage
from sqlalchemy import func, or_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Landing page"""
    # Get statistics for homepage
    total_lawyers = User.query.filter_by(role='lawyer').count()
    verified_lawyers = LawyerProfile.query.filter_by(verification_status='verified').count()
    total_customers = User.query.filter_by(role='customer').count()
    
    # Get statistics for laws
    total_acts = LegalAct.query.count()
    total_sections = LegalSection.query.count()
    
    # Get featured lawyers (verified, with profiles)
    featured_lawyers = db.session.query(User, LawyerProfile)\
        .join(LawyerProfile, User.id == LawyerProfile.user_id)\
        .filter(LawyerProfile.verification_status == 'verified')\
        .limit(3)\
        .all()
    
    return render_template('main/index.html',
                         title='Home',
                         total_lawyers=total_lawyers,
                         verified_lawyers=verified_lawyers,
                         total_customers=total_customers,
                         total_acts=total_acts,
                         total_sections=total_sections,
                         featured_lawyers=featured_lawyers)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html', title='About Us')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with working form"""
    errors = {}

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Validation
        if not name or len(name) < 2:
            errors['name'] = 'Name is required (min 2 characters).'
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = 'A valid email address is required.'
        if not subject or len(subject) < 3:
            errors['subject'] = 'Subject is required (min 3 characters).'
        if not message or len(message) < 10:
            errors['message'] = 'Message is required (min 10 characters).'

        if not errors:
            contact_msg = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))

    return render_template('main/contact.html', title='Contact Us', errors=errors)


@main_bp.route('/how-it-works')
def how_it_works():
    """How it works page"""
    return render_template('main/how_it_works.html', title='How It Works')


@main_bp.route('/browse-laws')
def browse_laws():
    """Browse Indian Laws - Main page (accessible without login)"""
    # Get filter parameters
    category = request.args.get('category', 'all')
    search_query = request.args.get('q', '')
    
    # Base query
    query = LegalAct.query
    
    # Apply category filter
    if category != 'all':
        query = query.filter_by(category=category)
    
    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                LegalAct.name.ilike(f'%{search_query}%'),
                LegalAct.short_name.ilike(f'%{search_query}%'),
                LegalAct.description.ilike(f'%{search_query}%')
            )
        )
    
    # Get all acts
    acts = query.order_by(LegalAct.year.desc()).all()
    
    # Get statistics
    total_acts = LegalAct.query.count()
    total_sections = LegalSection.query.count()
    
    # Get all unique categories
    categories = db.session.query(LegalAct.category).distinct().all()
    categories = [cat[0] for cat in categories]
    
    # Get popular sections (first 6 from IPC for now)
    popular_sections = LegalSection.query.join(LegalAct)\
        .filter(LegalAct.short_name == 'IPC')\
        .limit(6)\
        .all()
    
    return render_template('main/browse_laws.html',
                         title='Browse Indian Laws',
                         acts=acts,
                         total_acts=total_acts,
                         total_sections=total_sections,
                         categories=categories,
                         selected_category=category,
                         search_query=search_query,
                         popular_sections=popular_sections)


@main_bp.route('/browse-laws/act/<int:act_id>')
def view_act(act_id):
    """View specific legal act details (accessible without login)"""
    act = LegalAct.query.get_or_404(act_id)
    
    # Get search query for filtering sections
    search_query = request.args.get('q', '')
    
    # Get sections for this act
    sections_query = LegalSection.query.filter_by(act_id=act_id)
    
    # Apply search filter if provided
    if search_query:
        sections_query = sections_query.filter(
            or_(
                LegalSection.section_number.ilike(f'%{search_query}%'),
                LegalSection.title.ilike(f'%{search_query}%'),
                LegalSection.description.ilike(f'%{search_query}%'),
                LegalSection.keywords.ilike(f'%{search_query}%')
            )
        )
    
    sections = sections_query.order_by(LegalSection.section_number).all()
    
    # Get related acts (same category)
    related_acts = LegalAct.query\
        .filter(LegalAct.category == act.category, LegalAct.id != act.id)\
        .limit(3)\
        .all()
    
    return render_template('main/view_act.html',
                         title=f'{act.short_name} - {act.year}',
                         act=act,
                         sections=sections,
                         search_query=search_query,
                         related_acts=related_acts)


@main_bp.route('/browse-laws/section/<int:section_id>')
def view_section(section_id):
    """View specific section details (accessible without login)"""
    section = LegalSection.query.get_or_404(section_id)
    act = section.act
    
    # Get previous and next sections
    prev_section = LegalSection.query\
        .filter(LegalSection.act_id == act.id, LegalSection.id < section_id)\
        .order_by(LegalSection.id.desc())\
        .first()
    
    next_section = LegalSection.query\
        .filter(LegalSection.act_id == act.id, LegalSection.id > section_id)\
        .order_by(LegalSection.id.asc())\
        .first()
    
    # Get related sections (from same act, limit 5)
    related_sections = LegalSection.query\
        .filter(LegalSection.act_id == act.id, LegalSection.id != section_id)\
        .limit(5)\
        .all()
    
    return render_template('main/view_section.html',
                         title=f'Section {section.section_number} - {act.short_name}',
                         section=section,
                         act=act,
                         prev_section=prev_section,
                         next_section=next_section,
                         related_sections=related_sections)


@main_bp.route('/api/search-laws')
def search_laws():
    """AJAX endpoint for live search (accessible without login)"""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'acts': [], 'sections': []})
    
    # Search in acts
    acts = LegalAct.query.filter(
        or_(
            LegalAct.name.ilike(f'%{query}%'),
            LegalAct.short_name.ilike(f'%{query}%'),
            LegalAct.description.ilike(f'%{query}%')
        )
    ).limit(5).all()
    
    # Search in sections
    sections = LegalSection.query.filter(
        or_(
            LegalSection.section_number.ilike(f'%{query}%'),
            LegalSection.title.ilike(f'%{query}%'),
            LegalSection.description.ilike(f'%{query}%'),
            LegalSection.keywords.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    # Format results
    acts_data = [{
        'id': act.id,
        'name': act.name,
        'short_name': act.short_name,
        'year': act.year,
        'category': act.category,
        'url': f'/browse-laws/act/{act.id}'
    } for act in acts]
    
    sections_data = [{
        'id': section.id,
        'section_number': section.section_number,
        'title': section.title,
        'act_name': section.act.short_name,
        'url': f'/browse-laws/section/{section.id}'
    } for section in sections]
    
    return jsonify({
        'acts': acts_data,
        'sections': sections_data
    })


# ========== LEGAL PROBLEM ANALYZER ==========

@main_bp.route('/analyze-problem', methods=['GET', 'POST'])
def analyze_problem():
    """Legal Problem Analyzer - Analyze user's problem and find relevant laws"""
    if request.method == 'POST':
        problem_description = request.form.get('problem', '').strip()
        
        if not problem_description:
            return render_template('main/analyze_problem.html',
                                 title='Legal Problem Analyzer',
                                 error='Please describe your problem')
        
        # Analyze the problem and find matching laws
        results = analyze_legal_problem(problem_description)
        
        return render_template('main/analysis_results.html',
                             title='Analysis Results',
                             problem=problem_description,
                             results=results)
    
    return render_template('main/analyze_problem.html',
                         title='Legal Problem Analyzer')


def analyze_legal_problem(description):
    """
    Analyze user's problem description and find matching legal sections
    using keyword matching algorithm
    
    Args:
        description: User's problem description
        
    Returns:
        List of matching sections with relevance scores
    """
    # Convert to lowercase for case-insensitive matching
    description_lower = description.lower()
    
    # Get all sections with keywords
    all_sections = LegalSection.query.filter(LegalSection.keywords.isnot(None)).all()
    
    matching_sections = []
    
    for section in all_sections:
        if not section.keywords:
            continue
            
        # Split keywords and clean them
        keywords = [k.strip().lower() for k in section.keywords.split(',')]
        
        # Calculate match score
        score = 0
        matched_keywords = []
        
        for keyword in keywords:
            if keyword in description_lower:
                score += 1
                matched_keywords.append(keyword)
        
        # If there are matches, add to results
        if score > 0:
            matching_sections.append({
                'section': section,
                'act': section.act,
                'score': score,
                'matched_keywords': matched_keywords,
                'relevance_percentage': min(100, (score / len(keywords)) * 100)
            })
    
    # Sort by score (highest first)
    matching_sections.sort(key=lambda x: x['score'], reverse=True)
    
    # Return top 5 matches
    return matching_sections[:5]


@main_bp.route('/api/example-problems')
def get_example_problems():
    """Get example problems for quick fill"""
    examples = {
        'theft': 'Someone stole my mobile phone from my bag while I was traveling in the metro. The phone was worth ₹25,000 and had important personal data.',
        'assault': 'A person physically assaulted me during an argument and caused injuries to my face and arms. I have medical reports of the injuries.',
        'fraud': 'Someone cheated me by selling a fake gold chain claiming it was real 22-karat gold. I paid ₹50,000 for it but later found out it was fake.',
        'harassment': 'A person has been stalking me and sending inappropriate messages on social media. I feel threatened and unsafe.',
        'property': 'My neighbor has illegally occupied a portion of my land and refuses to vacate despite multiple requests.',
        'accident': 'A car hit me while I was crossing the road. The driver was driving rashly and did not stop after the accident.'
    }
    
    return jsonify(examples)
