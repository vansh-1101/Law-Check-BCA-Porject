"""
Simple Database Query Tool
"""
from app import create_app, db
from app.models import User, LawyerProfile, Consultation, Message, LegalAct, LegalSection
import json

def main():
    app = create_app()
    
    with app.app_context():
        print("\n=== DATABASE STATISTICS ===\n")
        
        # Count records
        user_count = User.query.count()
        lawyer_count = LawyerProfile.query.count()
        consultation_count = Consultation.query.count()
        message_count = Message.query.count()
        act_count = LegalAct.query.count()
        section_count = LegalSection.query.count()
        
        print(f"Users: {user_count}")
        print(f"Lawyer Profiles: {lawyer_count}")
        print(f"Consultations: {consultation_count}")
        print(f"Messages: {message_count}")
        print(f"Legal Acts: {act_count}")
        print(f"Legal Sections: {section_count}")
        
        print("\n=== USERS ===\n")
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Name: {user.full_name}")
            print(f"  Role: {user.role}")
            print(f"  Active: {user.is_active}")
            print()
        
        print("\n=== LEGAL ACTS ===\n")
        acts = LegalAct.query.all()
        for act in acts:
            print(f"{act.short_name} ({act.year}) - {act.name}")
            print(f"  Category: {act.category}")
            print(f"  Sections: {act.total_sections}")
            print()
        
        print("\n=== SAMPLE LEGAL SECTIONS (First 5) ===\n")
        sections = LegalSection.query.limit(5).all()
        for section in sections:
            print(f"Section {section.section_number} ({section.act.short_name})")
            print(f"  Title: {section.title}")
            print(f"  Bailable: {section.is_bailable}")
            print(f"  Cognizable: {section.is_cognizable}")
            print()

if __name__ == '__main__':
    main()
