"""
Interactive SQL Query Tool for Law Project Database
Run SQL queries directly on your database
"""
import sqlite3
import os
from tabulate import tabulate

# Database path
DB_PATH = os.path.join('instance', 'legal_platform.db')

def execute_query(query):
    """Execute SQL query and display results"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Execute query
        cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.strip().upper().startswith('SELECT'):
            # Fetch results
            results = cursor.fetchall()
            
            # Get column names
            columns = [description[0] for description in cursor.description]
            
            # Display results in table format
            if results:
                print("\n" + "="*80)
                print(tabulate(results, headers=columns, tablefmt='grid'))
                print(f"\nTotal rows: {len(results)}")
                print("="*80 + "\n")
            else:
                print("\nNo results found.\n")
        else:
            # For INSERT, UPDATE, DELETE
            conn.commit()
            print(f"\nQuery executed successfully. Rows affected: {cursor.rowcount}\n")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"\nError: {e}\n")

def show_tables():
    """Show all tables in database"""
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    execute_query(query)

def describe_table(table_name):
    """Show table structure"""
    query = f"PRAGMA table_info({table_name});"
    execute_query(query)

def main():
    """Main interactive menu"""
    print("\n" + "="*80)
    print("SQL QUERY TOOL - Law Project Database")
    print("="*80)
    
    while True:
        print("\nOptions:")
        print("1. Show all tables")
        print("2. Describe table structure")
        print("3. Run custom SQL query")
        print("4. Quick queries (pre-made)")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            print("\n--- All Tables ---")
            show_tables()
            
        elif choice == '2':
            table = input("Enter table name: ").strip()
            print(f"\n--- Structure of {table} ---")
            describe_table(table)
            
        elif choice == '3':
            print("\nEnter SQL query (press Enter twice to execute):")
            lines = []
            while True:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            query = ' '.join(lines)
            if query:
                execute_query(query)
            
        elif choice == '4':
            quick_queries_menu()
            
        elif choice == '5':
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid choice. Try again.")

def quick_queries_menu():
    """Pre-made queries for quick demonstration"""
    print("\n--- Quick Queries ---")
    print("1. Show all users")
    print("2. Show all legal acts")
    print("3. Show legal sections (first 10)")
    print("4. Count records in all tables")
    print("5. Show users by role")
    print("6. Show non-bailable offenses")
    print("7. Show cognizable offenses")
    print("8. Back to main menu")
    
    choice = input("\nEnter choice: ").strip()
    
    queries = {
        '1': "SELECT id, email, full_name, role, is_active FROM users;",
        '2': "SELECT id, short_name, name, year, category, total_sections FROM legal_acts;",
        '3': """
            SELECT 
                ls.section_number,
                la.short_name as act,
                ls.title,
                ls.is_bailable,
                ls.is_cognizable
            FROM legal_sections ls
            JOIN legal_acts la ON ls.act_id = la.id
            LIMIT 10;
        """,
        '4': """
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
        """,
        '5': """
            SELECT 
                role,
                COUNT(*) as total_users
            FROM users
            GROUP BY role;
        """,
        '6': """
            SELECT 
                la.short_name,
                ls.section_number,
                ls.title
            FROM legal_sections ls
            JOIN legal_acts la ON ls.act_id = la.id
            WHERE ls.is_bailable = 0;
        """,
        '7': """
            SELECT 
                la.short_name,
                ls.section_number,
                ls.title
            FROM legal_sections ls
            JOIN legal_acts la ON ls.act_id = la.id
            WHERE ls.is_cognizable = 1;
        """
    }
    
    if choice in queries:
        execute_query(queries[choice])
    elif choice == '8':
        return
    else:
        print("\nInvalid choice.")

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"\nError: Database not found at {DB_PATH}")
        print("Please run the application first to create the database.\n")
    else:
        main()
