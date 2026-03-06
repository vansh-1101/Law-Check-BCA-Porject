"""
Migration script to add new columns to legal_sections table
Run this to update existing database with penalty and legal status fields
"""
from app import create_app, db

def migrate_database():
    """Add new columns to legal_sections table"""
    app = create_app()
    
    with app.app_context():
        try:
            # Add new columns using raw SQL
            with db.engine.connect() as conn:
                # Check if columns already exist
                result = conn.execute(db.text("PRAGMA table_info(legal_sections)"))
                columns = [row[1] for row in result]
                
                if 'penalty' not in columns:
                    print("Adding 'penalty' column...")
                    conn.execute(db.text("ALTER TABLE legal_sections ADD COLUMN penalty TEXT"))
                    conn.commit()
                    print("✓ Added 'penalty' column")
                
                if 'is_bailable' not in columns:
                    print("Adding 'is_bailable' column...")
                    conn.execute(db.text("ALTER TABLE legal_sections ADD COLUMN is_bailable BOOLEAN DEFAULT 1"))
                    conn.commit()
                    print("✓ Added 'is_bailable' column")
                
                if 'is_cognizable' not in columns:
                    print("Adding 'is_cognizable' column...")
                    conn.execute(db.text("ALTER TABLE legal_sections ADD COLUMN is_cognizable BOOLEAN DEFAULT 0"))
                    conn.commit()
                    print("✓ Added 'is_cognizable' column")
                
                if 'is_compoundable' not in columns:
                    print("Adding 'is_compoundable' column...")
                    conn.execute(db.text("ALTER TABLE legal_sections ADD COLUMN is_compoundable BOOLEAN DEFAULT 0"))
                    conn.commit()
                    print("✓ Added 'is_compoundable' column")
            
            print("\n✅ Database migration completed successfully!")
            print("You can now run seed_laws.py to update the data.")
            
        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
