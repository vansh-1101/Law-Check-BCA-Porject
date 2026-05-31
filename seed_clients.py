"""
Seed script — creates 10 customer accounts in the database.
Run:  python seed_clients.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User

app = create_app()

CLIENTS = [
    {"full_name": "Aarav Sharma",    "email": "aarav.sharma@gmail.com",    "phone": "9876543210", "password": "Client@123"},
    {"full_name": "Priya Patel",     "email": "priya.patel@gmail.com",     "phone": "9876543211", "password": "Client@123"},
    {"full_name": "Rohan Mehta",     "email": "rohan.mehta@gmail.com",     "phone": "9876543212", "password": "Client@123"},
    {"full_name": "Sneha Gupta",     "email": "sneha.gupta@gmail.com",     "phone": "9876543213", "password": "Client@123"},
    {"full_name": "Vikram Singh",    "email": "vikram.singh@gmail.com",    "phone": "9876543214", "password": "Client@123"},
    {"full_name": "Ananya Reddy",    "email": "ananya.reddy@gmail.com",    "phone": "9876543215", "password": "Client@123"},
    {"full_name": "Karan Joshi",     "email": "karan.joshi@gmail.com",     "phone": "9876543216", "password": "Client@123"},
    {"full_name": "Meera Iyer",      "email": "meera.iyer@gmail.com",      "phone": "9876543217", "password": "Client@123"},
    {"full_name": "Arjun Desai",     "email": "arjun.desai@gmail.com",     "phone": "9876543218", "password": "Client@123"},
    {"full_name": "Divya Nair",      "email": "divya.nair@gmail.com",      "phone": "9876543219", "password": "Client@123"},
]

with app.app_context():
    created = []
    skipped = []

    for c in CLIENTS:
        if User.query.filter_by(email=c["email"]).first():
            skipped.append(c["email"])
            continue

        user = User(
            email=c["email"],
            full_name=c["full_name"],
            phone=c["phone"],
            role="customer",
            is_active=True,
        )
        user.set_password(c["password"])
        db.session.add(user)
        created.append(c["email"])

    db.session.commit()

    print(f"\n✅  Created {len(created)} client(s), skipped {len(skipped)} (already exist).\n")
    if skipped:
        print("Skipped:", ", ".join(skipped))
    print("\nDone!")
