"""
Script to check and display database contents
"""
import sys
from app import create_app, db
from app.models import User, LawyerProfile, Consultation, Message, LegalAct, LegalSection

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_database():
    """Display all database contents"""
    app = create_app()
    
    with app.app_context():
        print("\n" + "="*80)
        print("DATABASE CONTENTS CHECK")
        print("="*80)
        
        # Check Users
        print("\n[USERS TABLE]")
        print("-" * 80)
        users = User.query.all()
        print(f"Total Users: {len(users)}")
        for user in users:
            print(f"  ID: {user.id} | Email: {user.email} | Name: {user.full_name} | Role: {user.role} | Active: {user.is_active}")
        
        # Check Lawyer Profiles
        print("\n[LAWYER PROFILES TABLE]")
        print("-" * 80)
        lawyers = LawyerProfile.query.all()
        print(f"Total Lawyer Profiles: {len(lawyers)}")
        for lawyer in lawyers:
            print(f"  ID: {lawyer.id} | Bar Council ID: {lawyer.bar_council_id} | User: {lawyer.user.full_name} | Status: {lawyer.verification_status}")
        
        # Check Consultations
        print("\n[CONSULTATIONS TABLE]")
        print("-" * 80)
        consultations = Consultation.query.all()
        print(f"Total Consultations: {len(consultations)}")
        for consult in consultations:
            print(f"  ID: {consult.id} | Customer: {consult.customer.full_name} | Lawyer: {consult.lawyer.full_name} | Status: {consult.status}")
        
        # Check Messages
        print("\n[MESSAGES TABLE]")
        print("-" * 80)
        messages = Message.query.all()
        print(f"Total Messages: {len(messages)}")
        for msg in messages:
            print(f"  ID: {msg.id} | Consultation: {msg.consultation_id} | Sender: {msg.sender.full_name} | Read: {msg.is_read}")
        
        # Check Legal Acts
        print("\n[LEGAL ACTS TABLE]")
        print("-" * 80)
        acts = LegalAct.query.all()
        print(f"Total Legal Acts: {len(acts)}")
        for act in acts:
            print(f"  ID: {act.id} | {act.short_name} ({act.year}) | Category: {act.category} | Sections: {act.total_sections}")
        
        # Check Legal Sections
        print("\n[LEGAL SECTIONS TABLE]")
        print("-" * 80)
        sections = LegalSection.query.all()
        print(f"Total Legal Sections: {len(sections)}")
        
        # Show first 10 sections as sample
        print("\nSample Sections (first 10):")
        for section in sections[:10]:
            title = section.title[:60] if len(section.title) > 60 else section.title
            print(f"  Section {section.section_number} ({section.act.short_name}): {title}...")
        
        if len(sections) > 10:
            print(f"  ... and {len(sections) - 10} more sections")
        
        print("\n" + "="*80)
        print("DATABASE CHECK COMPLETE")
        print("="*80 + "\n")

if __name__ == '__main__':
    check_database()
