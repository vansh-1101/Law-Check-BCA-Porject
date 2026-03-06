# SQL Demonstration Queries for Exam Evaluator

## 📋 Overview
This document contains SQL queries to demonstrate your Law Project database to evaluators.

---

## 🗄️ Database Schema Overview

### Show All Tables
```sql
-- List all tables in database
SHOW TABLES;
```

**Expected Output:**
```
+---------------------------+
| Tables_in_legal_platform  |
+---------------------------+
| users                     |
| lawyer_profiles           |
| consultations             |
| messages                  |
| legal_acts                |
| legal_sections            |
+---------------------------+
```

---

## 📊 Table Structure Queries

### 1. Show USERS Table Structure
```sql
DESCRIBE users;
-- OR
SHOW COLUMNS FROM users;
```

**Expected Output:**
```
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int          | NO   | PRI | NULL    | auto_increment |
| email         | varchar(120) | NO   | UNI | NULL    |                |
| password_hash | varchar(255) | NO   |     | NULL    |                |
| full_name     | varchar(100) | NO   |     | NULL    |                |
| phone         | varchar(15)  | YES  |     | NULL    |                |
| role          | varchar(20)  | NO   |     | NULL    |                |
| is_active     | tinyint(1)   | YES  |     | 1       |                |
| created_at    | datetime     | YES  |     | NULL    |                |
+---------------+--------------+------+-----+---------+----------------+
```

### 2. Show LAWYER_PROFILES Table Structure
```sql
DESCRIBE lawyer_profiles;
```

### 3. Show CONSULTATIONS Table Structure
```sql
DESCRIBE consultations;
```

### 4. Show LEGAL_ACTS Table Structure
```sql
DESCRIBE legal_acts;
```

### 5. Show LEGAL_SECTIONS Table Structure
```sql
DESCRIBE legal_sections;
```

### 6. Show MESSAGES Table Structure
```sql
DESCRIBE messages;
```

---

## 🔍 Data Retrieval Queries

### View All Users
```sql
SELECT * FROM users;
```

**Better formatted query:**
```sql
SELECT 
    id,
    email,
    full_name,
    role,
    is_active,
    DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') as created_date
FROM users;
```

### View Users by Role
```sql
-- Show all admins
SELECT * FROM users WHERE role = 'admin';

-- Show all lawyers
SELECT * FROM users WHERE role = 'lawyer';

-- Show all customers
SELECT * FROM users WHERE role = 'customer';
```

### Count Users by Role
```sql
SELECT 
    role,
    COUNT(*) as total_users
FROM users
GROUP BY role;
```

**Expected Output:**
```
+----------+-------------+
| role     | total_users |
+----------+-------------+
| admin    | 1           |
| lawyer   | 1           |
| customer | 1           |
+----------+-------------+
```

---

## ⚖️ Legal Acts Queries

### View All Legal Acts
```sql
SELECT * FROM legal_acts;
```

**Better formatted:**
```sql
SELECT 
    id,
    short_name,
    name,
    year,
    category,
    total_sections
FROM legal_acts
ORDER BY year;
```

### Count Acts by Category
```sql
SELECT 
    category,
    COUNT(*) as total_acts
FROM legal_acts
GROUP BY category;
```

### Find Specific Act
```sql
-- Find IPC
SELECT * FROM legal_acts WHERE short_name = 'IPC';

-- Find all Criminal laws
SELECT * FROM legal_acts WHERE category = 'Criminal';
```

---

## 📜 Legal Sections Queries

### View All Sections
```sql
SELECT * FROM legal_sections LIMIT 10;
```

**Better formatted with Act name:**
```sql
SELECT 
    ls.id,
    la.short_name as act,
    ls.section_number,
    ls.title,
    ls.is_bailable,
    ls.is_cognizable
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
LIMIT 10;
```

### Find Specific Section
```sql
-- Find Section 302 IPC
SELECT 
    ls.*,
    la.short_name as act_name
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
WHERE ls.section_number = '302' AND la.short_name = 'IPC';
```

### Count Sections by Act
```sql
SELECT 
    la.short_name,
    COUNT(ls.id) as total_sections
FROM legal_acts la
LEFT JOIN legal_sections ls ON la.id = ls.act_id
GROUP BY la.id, la.short_name;
```

### Find Non-Bailable Offenses
```sql
SELECT 
    la.short_name,
    ls.section_number,
    ls.title,
    ls.penalty
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
WHERE ls.is_bailable = 0;
```

### Find Cognizable Offenses
```sql
SELECT 
    la.short_name,
    ls.section_number,
    ls.title
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
WHERE ls.is_cognizable = 1;
```

---

## 👥 User & Lawyer Profile Queries

### View Lawyers with Profiles
```sql
SELECT 
    u.id,
    u.full_name,
    u.email,
    lp.bar_council_id,
    lp.experience_years,
    lp.consultation_fee,
    lp.verification_status
FROM users u
LEFT JOIN lawyer_profiles lp ON u.id = lp.user_id
WHERE u.role = 'lawyer';
```

### Count Verified Lawyers
```sql
SELECT 
    verification_status,
    COUNT(*) as total
FROM lawyer_profiles
GROUP BY verification_status;
```

---

## 📅 Consultation Queries

### View All Consultations
```sql
SELECT 
    c.id,
    customer.full_name as customer_name,
    lawyer.full_name as lawyer_name,
    c.consultation_date,
    c.category,
    c.status
FROM consultations c
JOIN users customer ON c.customer_id = customer.id
JOIN users lawyer ON c.lawyer_id = lawyer.id;
```

### Count Consultations by Status
```sql
SELECT 
    status,
    COUNT(*) as total
FROM consultations
GROUP BY status;
```

### Find Pending Consultations
```sql
SELECT * FROM consultations WHERE status = 'pending';
```

---

## 💬 Message Queries

### View Messages in a Consultation
```sql
SELECT 
    m.id,
    u.full_name as sender,
    m.message,
    m.is_read,
    m.created_at
FROM messages m
JOIN users u ON m.sender_id = u.id
WHERE m.consultation_id = 1
ORDER BY m.created_at;
```

### Count Unread Messages
```sql
SELECT 
    COUNT(*) as unread_messages
FROM messages
WHERE is_read = 0;
```

---

## 📊 Advanced Queries (To Impress Evaluator)

### 1. Most Popular Legal Categories
```sql
SELECT 
    category,
    COUNT(*) as total_acts,
    SUM(total_sections) as total_sections
FROM legal_acts
GROUP BY category
ORDER BY total_acts DESC;
```

### 2. User Activity Summary
```sql
SELECT 
    role,
    COUNT(*) as total_users,
    SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_users,
    SUM(CASE WHEN is_active = 0 THEN 1 ELSE 0 END) as inactive_users
FROM users
GROUP BY role;
```

### 3. Lawyer Performance Report
```sql
SELECT 
    u.full_name as lawyer_name,
    COUNT(c.id) as total_consultations,
    SUM(CASE WHEN c.status = 'completed' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN c.status = 'pending' THEN 1 ELSE 0 END) as pending
FROM users u
LEFT JOIN consultations c ON u.id = c.lawyer_id
WHERE u.role = 'lawyer'
GROUP BY u.id, u.full_name;
```

### 4. Search Sections by Keyword
```sql
SELECT 
    la.short_name,
    ls.section_number,
    ls.title
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
WHERE ls.title LIKE '%murder%' 
   OR ls.keywords LIKE '%murder%';
```

### 5. Complete Database Statistics
```sql
SELECT 
    'Users' as table_name, COUNT(*) as total FROM users
UNION ALL
SELECT 'Lawyer Profiles', COUNT(*) FROM lawyer_profiles
UNION ALL
SELECT 'Consultations', COUNT(*) FROM consultations
UNION ALL
SELECT 'Messages', COUNT(*) FROM messages
UNION ALL
SELECT 'Legal Acts', COUNT(*) FROM legal_acts
UNION ALL
SELECT 'Legal Sections', COUNT(*) FROM legal_sections;
```

---

## 🔐 Database Relationships (Foreign Keys)

### Show Foreign Key Constraints
```sql
-- For MySQL
SELECT 
    TABLE_NAME,
    COLUMN_NAME,
    CONSTRAINT_NAME,
    REFERENCED_TABLE_NAME,
    REFERENCED_COLUMN_NAME
FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'legal_platform'
  AND REFERENCED_TABLE_NAME IS NOT NULL;
```

---

## 📈 Data Insertion Examples (If Evaluator Asks)

### Insert New User
```sql
INSERT INTO users (email, password_hash, full_name, phone, role, is_active, created_at)
VALUES (
    'john.doe@example.com',
    'hashed_password_here',
    'John Doe',
    '9876543210',
    'customer',
    1,
    NOW()
);
```

### Insert Legal Section
```sql
INSERT INTO legal_sections (
    act_id, 
    section_number, 
    title, 
    description, 
    keywords,
    penalty,
    is_bailable,
    is_cognizable,
    is_compoundable
)
VALUES (
    1,  -- IPC act_id
    '498A',
    'Husband or Relative of Husband Subjecting Woman to Cruelty',
    'Full description here...',
    'dowry,cruelty,harassment',
    'Imprisonment up to 3 years and fine',
    0,  -- Non-bailable
    1,  -- Cognizable
    0   -- Non-compoundable
);
```

---

## 🎯 Quick Demo Script for Evaluator

```sql
-- 1. Show database structure
SHOW TABLES;

-- 2. Show user data
SELECT id, email, full_name, role FROM users;

-- 3. Show legal acts
SELECT short_name, name, year, category FROM legal_acts;

-- 4. Show sample sections with act names
SELECT 
    la.short_name,
    ls.section_number,
    ls.title,
    ls.is_bailable,
    ls.is_cognizable
FROM legal_sections ls
JOIN legal_acts la ON ls.act_id = la.id
LIMIT 5;

-- 5. Show database statistics
SELECT 
    'Users' as entity, COUNT(*) as count FROM users
UNION ALL
SELECT 'Legal Acts', COUNT(*) FROM legal_acts
UNION ALL
SELECT 'Legal Sections', COUNT(*) FROM legal_sections;
```

---

## 💡 Tips for Presentation

1. **Start Simple:** Begin with `SHOW TABLES` and `DESCRIBE` commands
2. **Show Relationships:** Demonstrate JOIN queries
3. **Highlight Features:** Show the legal analyzer fields (is_bailable, is_cognizable)
4. **Be Ready:** Know the purpose of each table
5. **Explain Design:** Mention normalization and foreign key relationships

---

## 🚀 How to Access MySQL Command Line

If you need to switch to MySQL:

1. **Install MySQL** (if not already)
2. **Export SQLite to MySQL:**
   ```bash
   # Use migration script
   python migrate_to_mysql.py
   ```
3. **Access MySQL:**
   ```bash
   mysql -u root -p
   USE legal_platform;
   ```

---

## ⚠️ Important Notes

- Your current database is **SQLite** (file-based)
- All these queries work in **MySQL/MariaDB** too
- For SQLite command line: `sqlite3 instance/legal_platform.db`
- The syntax is 99% compatible between SQLite and MySQL
