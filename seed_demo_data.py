"""
Seed demo data: 10 Customers + 10 Lawyers + 1 Admin
Clears existing users and lawyer profiles first.
"""
import json
from app import create_app, db
from app.models import User, LawyerProfile, Message, Consultation

app = create_app()

with app.app_context():
    # Delete in correct order to avoid foreign key issues
    print("🗑️  Clearing existing data...")
    Message.query.delete()
    Consultation.query.delete()
    LawyerProfile.query.delete()
    User.query.delete()
    db.session.commit()
    print("✅ All users, lawyers, consultations, and messages deleted.\n")

    # ── 1 Admin ──
    admin = User(
        email='admin@legalconnect.in',
        full_name='Admin User',
        phone='9000000000',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)

    # ── 10 Customers ──
    customers_data = [
        {'email': 'rahul.sharma@gmail.com',   'full_name': 'Rahul Sharma',     'phone': '9876543210'},
        {'email': 'priya.patel@gmail.com',     'full_name': 'Priya Patel',      'phone': '9876543211'},
        {'email': 'amit.kumar@gmail.com',      'full_name': 'Amit Kumar',       'phone': '9876543212'},
        {'email': 'sneha.reddy@gmail.com',     'full_name': 'Sneha Reddy',      'phone': '9876543213'},
        {'email': 'vikram.singh@gmail.com',    'full_name': 'Vikram Singh',     'phone': '9876543214'},
        {'email': 'ananya.gupta@gmail.com',    'full_name': 'Ananya Gupta',     'phone': '9876543215'},
        {'email': 'rohit.verma@gmail.com',     'full_name': 'Rohit Verma',      'phone': '9876543216'},
        {'email': 'deepika.nair@gmail.com',    'full_name': 'Deepika Nair',     'phone': '9876543217'},
        {'email': 'arjun.mehta@gmail.com',     'full_name': 'Arjun Mehta',      'phone': '9876543218'},
        {'email': 'kavita.joshi@gmail.com',    'full_name': 'Kavita Joshi',     'phone': '9876543219'},
    ]

    print("👤 Creating 10 customers...")
    for c in customers_data:
        user = User(
            email=c['email'],
            full_name=c['full_name'],
            phone=c['phone'],
            role='customer',
            is_active=True
        )
        user.set_password('customer123')
        db.session.add(user)
    db.session.commit()
    print("✅ 10 customers created.\n")

    # ── 10 Lawyers ──
    lawyers_data = [
        {
            'email': 'adv.rajan.pillai@gmail.com',   'full_name': 'Adv. Rajan Pillai',
            'phone': '9900000001', 'bar_id': 'MH/1234/2015',
            'specializations': '["Criminal Law", "Bail Matters"]',
            'experience': 9, 'education': 'LLB, Mumbai University',
            'languages': '["Hindi", "English", "Marathi"]', 'fee': 2000,
            'bio': 'Experienced criminal lawyer practicing in Mumbai High Court.'
        },
        {
            'email': 'adv.meera.iyer@gmail.com',     'full_name': 'Adv. Meera Iyer',
            'phone': '9900000002', 'bar_id': 'KA/5678/2016',
            'specializations': '["Family Law", "Divorce", "Child Custody"]',
            'experience': 7, 'education': 'LLB, Bangalore University',
            'languages': '["Hindi", "English", "Kannada"]', 'fee': 1500,
            'bio': 'Family law expert specializing in divorce and custody cases.'
        },
        {
            'email': 'adv.sanjay.deshmukh@gmail.com','full_name': 'Adv. Sanjay Deshmukh',
            'phone': '9900000003', 'bar_id': 'MH/9012/2014',
            'specializations': '["Corporate Law", "Company Registration"]',
            'experience': 10, 'education': 'LLM, Pune University',
            'languages': '["Hindi", "English", "Marathi"]', 'fee': 3000,
            'bio': 'Corporate law specialist handling company formations and mergers.'
        },
        {
            'email': 'adv.fatima.khan@gmail.com',    'full_name': 'Adv. Fatima Khan',
            'phone': '9900000004', 'bar_id': 'DL/3456/2017',
            'specializations': '["Civil Law", "Property Disputes"]',
            'experience': 6, 'education': 'LLB, Delhi University',
            'languages': '["Hindi", "English", "Urdu"]', 'fee': 1800,
            'bio': 'Civil litigation expert with focus on property and land disputes.'
        },
        {
            'email': 'adv.karthik.ram@gmail.com',    'full_name': 'Adv. Karthik Ram',
            'phone': '9900000005', 'bar_id': 'TN/7890/2013',
            'specializations': '["Constitutional Law", "PIL"]',
            'experience': 11, 'education': 'LLM, Madras Law College',
            'languages': '["Hindi", "English", "Tamil"]', 'fee': 2500,
            'bio': 'Constitutional law expert practicing in Madras High Court.'
        },
        {
            'email': 'adv.nisha.agarwal@gmail.com',  'full_name': 'Adv. Nisha Agarwal',
            'phone': '9900000006', 'bar_id': 'UP/1122/2018',
            'specializations': '["Cyber Law", "IT Act"]',
            'experience': 5, 'education': 'LLB, Lucknow University',
            'languages': '["Hindi", "English"]', 'fee': 1200,
            'bio': 'Cyber law specialist handling online fraud and IT act cases.'
        },
        {
            'email': 'adv.harsh.trivedi@gmail.com',  'full_name': 'Adv. Harsh Trivedi',
            'phone': '9900000007', 'bar_id': 'GJ/3344/2015',
            'specializations': '["Labour Law", "Employment Disputes"]',
            'experience': 8, 'education': 'LLB, Gujarat University',
            'languages': '["Hindi", "English", "Gujarati"]', 'fee': 1600,
            'bio': 'Labour law expert advising on employment disputes and worker rights.'
        },
        {
            'email': 'adv.rekha.menon@gmail.com',    'full_name': 'Adv. Rekha Menon',
            'phone': '9900000008', 'bar_id': 'KL/5566/2016',
            'specializations': '["Consumer Law", "Consumer Protection"]',
            'experience': 7, 'education': 'LLB, Kerala University',
            'languages': '["Hindi", "English", "Malayalam"]', 'fee': 1400,
            'bio': 'Consumer rights advocate handling product liability and fraud cases.'
        },
        {
            'email': 'adv.dev.chauhan@gmail.com',    'full_name': 'Adv. Dev Chauhan',
            'phone': '9900000009', 'bar_id': 'RJ/7788/2012',
            'specializations': '["Tax Law", "GST", "Income Tax"]',
            'experience': 12, 'education': 'LLM, Rajasthan University',
            'languages': '["Hindi", "English"]', 'fee': 3500,
            'bio': 'Senior tax consultant with expertise in GST and income tax litigation.'
        },
        {
            'email': 'adv.pooja.bhat@gmail.com',     'full_name': 'Adv. Pooja Bhat',
            'phone': '9900000010', 'bar_id': 'WB/9900/2019',
            'specializations': '["Immigration Law", "Visa Issues"]',
            'experience': 4, 'education': 'LLB, Calcutta University',
            'languages': '["Hindi", "English", "Bengali"]', 'fee': 2000,
            'bio': 'Immigration law specialist helping with visa and citizenship matters.'
        },
    ]

    print("⚖️  Creating 10 lawyers with profiles...")
    for l in lawyers_data:
        user = User(
            email=l['email'],
            full_name=l['full_name'],
            phone=l['phone'],
            role='lawyer',
            is_active=True
        )
        user.set_password('lawyer123')
        db.session.add(user)
        db.session.flush()  # get user.id

        profile = LawyerProfile(
            user_id=user.id,
            bar_council_id=l['bar_id'],
            specializations=l['specializations'],
            experience_years=l['experience'],
            education=l['education'],
            languages=l['languages'],
            consultation_fee=l['fee'],
            verification_status='verified',
            bio=l['bio']
        )
        db.session.add(profile)

    db.session.commit()
    print("✅ 10 lawyers created with profiles.\n")

    # ── Summary ──
    total_users = User.query.count()
    total_customers = User.query.filter_by(role='customer').count()
    total_lawyers = User.query.filter_by(role='lawyer').count()
    total_admins = User.query.filter_by(role='admin').count()
    total_profiles = LawyerProfile.query.count()

    print("=" * 50)
    print(f"📊 SUMMARY")
    print(f"   Total users     : {total_users}")
    print(f"   Admins          : {total_admins}")
    print(f"   Customers       : {total_customers}")
    print(f"   Lawyers         : {total_lawyers}")
    print(f"   Lawyer profiles : {total_profiles}")
    print("=" * 50)
    print(f"\n🎉 Demo data seeded! Check phpMyAdmin to see the tables.")
    print(f"\n🔑 Login credentials:")
    print(f"   Admin    : admin@legalconnect.in / admin123")
    print(f"   Customer : rahul.sharma@gmail.com / customer123")
    print(f"   Lawyer   : adv.rajan.pillai@gmail.com / lawyer123")
