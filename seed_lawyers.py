"""
Seed script — creates 10 verified lawyer accounts in the database.
Run:  python seed_lawyers.py
"""
import sys, os, json, secrets
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User, LawyerProfile, LawyerPayment

app = create_app()

LAWYERS = [
    {"full_name": "Adv. Rajesh Kumar",     "email": "rajesh.kumar@lawfirm.com",     "phone": "9800000001", "password": "Lawyer@123", "bar_id": "BAR/MH/2018/001", "specializations": ["Criminal Law", "Constitutional Law"],  "experience": 8},
    {"full_name": "Adv. Neha Verma",       "email": "neha.verma@lawfirm.com",       "phone": "9800000002", "password": "Lawyer@123", "bar_id": "BAR/DL/2019/002", "specializations": ["Family Law", "Divorce Law"],           "experience": 6},
    {"full_name": "Adv. Sanjay Mishra",    "email": "sanjay.mishra@lawfirm.com",    "phone": "9800000003", "password": "Lawyer@123", "bar_id": "BAR/UP/2016/003", "specializations": ["Corporate Law", "Tax Law"],            "experience": 10},
    {"full_name": "Adv. Kavita Rao",       "email": "kavita.rao@lawfirm.com",       "phone": "9800000004", "password": "Lawyer@123", "bar_id": "BAR/KA/2020/004", "specializations": ["Civil Law", "Property Law"],           "experience": 5},
    {"full_name": "Adv. Amit Tiwari",      "email": "amit.tiwari@lawfirm.com",      "phone": "9800000005", "password": "Lawyer@123", "bar_id": "BAR/RJ/2017/005", "specializations": ["Cyber Law", "IT Law"],                 "experience": 7},
    {"full_name": "Adv. Pooja Bhatt",      "email": "pooja.bhatt@lawfirm.com",      "phone": "9800000006", "password": "Lawyer@123", "bar_id": "BAR/GJ/2015/006", "specializations": ["Labor Law", "Consumer Law"],           "experience": 11},
    {"full_name": "Adv. Deepak Chauhan",   "email": "deepak.chauhan@lawfirm.com",   "phone": "9800000007", "password": "Lawyer@123", "bar_id": "BAR/MP/2021/007", "specializations": ["Criminal Law", "NDPS Law"],            "experience": 4},
    {"full_name": "Adv. Sunita Pillai",    "email": "sunita.pillai@lawfirm.com",    "phone": "9800000008", "password": "Lawyer@123", "bar_id": "BAR/KL/2014/008", "specializations": ["Human Rights", "PIL"],                 "experience": 12},
    {"full_name": "Adv. Manish Agarwal",   "email": "manish.agarwal@lawfirm.com",   "phone": "9800000009", "password": "Lawyer@123", "bar_id": "BAR/WB/2019/009", "specializations": ["Banking Law", "Corporate Law"],       "experience": 6},
    {"full_name": "Adv. Ritu Saxena",      "email": "ritu.saxena@lawfirm.com",      "phone": "9800000010", "password": "Lawyer@123", "bar_id": "BAR/TN/2018/010", "specializations": ["Intellectual Property", "Environmental Law"], "experience": 8},
]

with app.app_context():
    created = []
    skipped = []

    for l in LAWYERS:
        if User.query.filter_by(email=l["email"]).first():
            skipped.append(l["email"])
            continue

        # Create user
        user = User(
            email=l["email"],
            full_name=l["full_name"],
            phone=l["phone"],
            role="lawyer",
            is_active=True,
        )
        user.set_password(l["password"])
        db.session.add(user)
        db.session.flush()  # get user.id

        # Create lawyer profile (already verified)
        profile = LawyerProfile(
            user_id=user.id,
            bar_council_id=l["bar_id"],
            specializations=json.dumps(l["specializations"]),
            experience_years=l["experience"],
            verification_status="verified",
        )
        db.session.add(profile)

        # Create completed payment record
        payment = LawyerPayment(
            user_id=user.id,
            amount=2.0,
            payment_type="membership",
            payment_method="card",
            transaction_id="SEED-" + secrets.token_hex(10).upper(),
            status="completed",
            order_token=secrets.token_hex(32),
        )
        db.session.add(payment)

        created.append(l["email"])

    db.session.commit()

    print(f"\n✅  Created {len(created)} lawyer(s), skipped {len(skipped)} (already exist).\n")
    if skipped:
        print("Skipped:", ", ".join(skipped))
    print("\nDone!")
