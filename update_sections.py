"""
Update existing legal sections with penalty and legal status information
Run this after migrate_database.py
"""
from app import create_app, db
from app.models import LegalSection

def update_section_data():
    """Update existing sections with penalty and legal status"""
    app = create_app()
    
    with app.app_context():
        print("🔄 Updating legal sections with penalty and status information...")
        
        # Define updates for key sections
        updates = {
            '302': {  # Murder
                'keywords': 'murder, death penalty, life imprisonment, homicide, killing, killed, murderer, culpable homicide, intentional killing, death, dead',
                'penalty': 'Death penalty or life imprisonment and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '307': {  # Attempt to Murder
                'keywords': 'attempt to murder, attempted homicide, intention to kill, tried to kill, attack, assault, life-threatening, weapon attack',
                'penalty': 'Imprisonment up to 10 years and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '323': {  # Voluntarily Causing Hurt
                'keywords': 'hurt, assault, beating, physical violence, injury, injured, hit, punch, kick, slap, fight, attacked, violence, bodily harm, bruises, wounds',
                'penalty': 'Imprisonment up to 1 year, or fine up to ₹1000, or both',
                'is_bailable': True,
                'is_cognizable': False,
                'is_compoundable': True
            },
            '354': {  # Assault on Woman
                'keywords': 'molestation, assault on women, modesty, sexual harassment, touched, groped, inappropriate touch, eve teasing, stalking, harassment',
                'penalty': 'Imprisonment from 1 to 5 years and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '379': {  # Theft
                'keywords': 'theft, stealing, larceny, property crime, stole, stolen, took, taking, dishonestly, movable property, without consent, thief, robbed, robbery, phone theft, mobile theft, wallet theft, bag theft, purse theft',
                'penalty': 'Imprisonment up to 3 years, or fine, or both',
                'is_bailable': True,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '420': {  # Cheating
                'keywords': 'cheating, fraud, dishonesty, deception, property, cheat, cheated, fraudulent, scam, conned, tricked, deceived, fake, counterfeit, forgery, false promise',
                'penalty': 'Imprisonment up to 7 years and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '376': {  # Rape
                'keywords': 'rape, sexual assault, sexual violence, women safety, forced intercourse, sexual abuse',
                'penalty': 'Rigorous imprisonment minimum 10 years, may extend to life imprisonment and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            },
            '498A': {  # Cruelty by Husband
                'keywords': 'domestic violence, cruelty, dowry harassment, women protection, husband cruelty, marital abuse',
                'penalty': 'Imprisonment up to 3 years and fine',
                'is_bailable': False,
                'is_cognizable': True,
                'is_compoundable': False
            }
        }
        
        updated_count = 0
        
        for section_number, data in updates.items():
            section = LegalSection.query.filter_by(section_number=section_number).first()
            
            if section:
                section.keywords = data['keywords']
                section.penalty = data['penalty']
                section.is_bailable = data['is_bailable']
                section.is_cognizable = data['is_cognizable']
                section.is_compoundable = data['is_compoundable']
                updated_count += 1
                print(f"✓ Updated IPC Section {section_number} - {section.title}")
        
        db.session.commit()
        
        print(f"\n✅ Successfully updated {updated_count} sections!")
        print("Legal Problem Analyzer is now ready to use!")

if __name__ == '__main__':
    update_section_data()
