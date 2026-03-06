"""
Generate SQL Demonstration File for Exam Evaluator
Creates a complete SQL file showing database structure and sample queries
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join('instance', 'legal_platform.db')
OUTPUT_FILE = 'database_demonstration.sql'

def generate_sql_demo():
    """Generate comprehensive SQL demonstration file"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Header
        f.write("-- ============================================================================\n")
        f.write("-- LAW PROJECT DATABASE DEMONSTRATION\n")
        f.write(f"-- Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- Database: Legal Consultation Platform\n")
        f.write("-- ============================================================================\n\n")
        
        # Database overview
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 1: DATABASE OVERVIEW\n")
        f.write("-- ============================================================================\n\n")
        
        # Show all tables
        f.write("-- List all tables\n")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        f.write("-- Tables in database:\n")
        for table in tables:
            f.write(f"--   - {table[0]}\n")
        f.write("\n")
        
        # Table structures
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 2: TABLE STRUCTURES\n")
        f.write("-- ============================================================================\n\n")
        
        for table in tables:
            table_name = table[0]
            f.write(f"-- Table: {table_name}\n")
            f.write(f"-- ----------------------------------------------------------------------------\n")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            f.write(f"-- Columns:\n")
            for col in columns:
                col_id, name, type_, notnull, default, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                null_str = " NOT NULL" if notnull else ""
                f.write(f"--   {name}: {type_}{null_str}{pk_str}\n")
            
            f.write("\n")
        
        # Data statistics
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 3: DATA STATISTICS\n")
        f.write("-- ============================================================================\n\n")
        
        f.write("-- Record counts in each table:\n")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            f.write(f"-- {table_name}: {count} records\n")
        f.write("\n")
        
        # Sample queries
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 4: SAMPLE QUERIES\n")
        f.write("-- ============================================================================\n\n")
        
        # Query 1: Show all users
        f.write("-- Query 1: Display all users\n")
        f.write("SELECT id, email, full_name, role, is_active FROM users;\n\n")
        
        cursor.execute("SELECT id, email, full_name, role, is_active FROM users;")
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Query 2: Show legal acts
        f.write("-- Query 2: Display all legal acts\n")
        f.write("SELECT id, short_name, name, year, category, total_sections FROM legal_acts;\n\n")
        
        cursor.execute("SELECT id, short_name, name, year, category, total_sections FROM legal_acts;")
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Query 3: Show sections with act names
        f.write("-- Query 3: Display legal sections with act names (first 10)\n")
        query = """
        SELECT 
            la.short_name,
            ls.section_number,
            ls.title,
            ls.is_bailable,
            ls.is_cognizable
        FROM legal_sections ls
        JOIN legal_acts la ON ls.act_id = la.id
        LIMIT 10;
        """
        f.write(query + "\n")
        
        cursor.execute(query)
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Query 4: Count users by role
        f.write("-- Query 4: Count users by role\n")
        query = "SELECT role, COUNT(*) as total FROM users GROUP BY role;"
        f.write(query + "\n\n")
        
        cursor.execute(query)
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Query 5: Non-bailable offenses
        f.write("-- Query 5: Find non-bailable offenses\n")
        query = """
        SELECT 
            la.short_name,
            ls.section_number,
            ls.title
        FROM legal_sections ls
        JOIN legal_acts la ON ls.act_id = la.id
        WHERE ls.is_bailable = 0;
        """
        f.write(query + "\n")
        
        cursor.execute(query)
        results = cursor.fetchall()
        f.write(f"-- Total non-bailable offenses: {len(results)}\n")
        f.write("-- Sample results:\n")
        for row in results[:5]:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Advanced queries
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 5: ADVANCED QUERIES (To Impress Evaluator)\n")
        f.write("-- ============================================================================\n\n")
        
        # Query 6: Complete statistics
        f.write("-- Query 6: Complete database statistics\n")
        query = """
        SELECT 'users' as table_name, COUNT(*) as count FROM users
        UNION ALL
        SELECT 'lawyer_profiles', COUNT(*) FROM lawyer_profiles
        UNION ALL
        SELECT 'consultations', COUNT(*) FROM consultations
        UNION ALL
        SELECT 'messages', COUNT(*) FROM messages
        UNION ALL
        SELECT 'legal_acts', COUNT(*) FROM legal_acts
        UNION ALL
        SELECT 'legal_sections', COUNT(*) FROM legal_sections;
        """
        f.write(query + "\n")
        
        cursor.execute(query)
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Query 7: Acts by category
        f.write("-- Query 7: Group legal acts by category\n")
        query = """
        SELECT 
            category,
            COUNT(*) as total_acts,
            SUM(total_sections) as total_sections
        FROM legal_acts
        GROUP BY category;
        """
        f.write(query + "\n")
        
        cursor.execute(query)
        results = cursor.fetchall()
        f.write("-- Results:\n")
        for row in results:
            f.write(f"-- {row}\n")
        f.write("\n")
        
        # Sample data
        f.write("-- ============================================================================\n")
        f.write("-- SECTION 6: SAMPLE DATA (First 5 records from each table)\n")
        f.write("-- ============================================================================\n\n")
        
        for table in tables:
            table_name = table[0]
            f.write(f"-- Sample data from {table_name}:\n")
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            results = cursor.fetchall()
            
            if results:
                # Get column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [col[1] for col in cursor.fetchall()]
                f.write(f"-- Columns: {', '.join(columns)}\n")
                
                for row in results:
                    f.write(f"-- {row}\n")
            else:
                f.write("-- (No data)\n")
            f.write("\n")
        
        # Footer
        f.write("-- ============================================================================\n")
        f.write("-- END OF DEMONSTRATION\n")
        f.write("-- ============================================================================\n")
    
    conn.close()
    
    print("\n" + "="*80)
    print("SQL DEMONSTRATION FILE GENERATED SUCCESSFULLY!")
    print("="*80)
    print(f"\nFile saved: {OUTPUT_FILE}")
    print("\nThis file contains:")
    print("  - Database structure (all tables and columns)")
    print("  - Data statistics")
    print("  - Sample SQL queries with results")
    print("  - Advanced queries to impress evaluator")
    print("\nYou can open this file and show it to your evaluator!")
    print("="*80 + "\n")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"\nError: Database not found at {DB_PATH}")
        print("Please run the application first.\n")
    else:
        generate_sql_demo()
