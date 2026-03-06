-- ============================================================================
-- LAW PROJECT DATABASE DEMONSTRATION
-- Generated on: 2026-01-31 07:05:22
-- Database: Legal Consultation Platform
-- ============================================================================

-- ============================================================================
-- SECTION 1: DATABASE OVERVIEW
-- ============================================================================

-- List all tables
-- Tables in database:
--   - consultations
--   - lawyer_profiles
--   - legal_acts
--   - legal_sections
--   - messages
--   - users

-- ============================================================================
-- SECTION 2: TABLE STRUCTURES
-- ============================================================================

-- Table: consultations
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   customer_id: INTEGER NOT NULL
--   lawyer_id: INTEGER NOT NULL
--   consultation_date: DATETIME NOT NULL
--   issue_description: TEXT NOT NULL
--   category: VARCHAR(50)
--   status: VARCHAR(20)
--   created_at: DATETIME
--   updated_at: DATETIME

-- Table: lawyer_profiles
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   user_id: INTEGER NOT NULL
--   bar_council_id: VARCHAR(50) NOT NULL
--   specializations: TEXT
--   experience_years: INTEGER
--   education: TEXT
--   languages: TEXT
--   consultation_fee: FLOAT
--   verification_status: VARCHAR(20)
--   bio: TEXT
--   profile_image: VARCHAR(255)
--   credentials_document: VARCHAR(255)
--   created_at: DATETIME
--   updated_at: DATETIME

-- Table: legal_acts
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   name: VARCHAR(200) NOT NULL
--   short_name: VARCHAR(50) NOT NULL
--   year: INTEGER NOT NULL
--   category: VARCHAR(50) NOT NULL
--   description: TEXT
--   total_sections: INTEGER
--   created_at: DATETIME

-- Table: legal_sections
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   act_id: INTEGER NOT NULL
--   section_number: VARCHAR(20) NOT NULL
--   title: VARCHAR(500) NOT NULL
--   description: TEXT NOT NULL
--   keywords: TEXT
--   created_at: DATETIME
--   penalty: TEXT
--   is_bailable: BOOLEAN
--   is_cognizable: BOOLEAN
--   is_compoundable: BOOLEAN

-- Table: messages
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   consultation_id: INTEGER NOT NULL
--   sender_id: INTEGER NOT NULL
--   message: TEXT NOT NULL
--   is_read: BOOLEAN
--   created_at: DATETIME

-- Table: users
-- ----------------------------------------------------------------------------
-- Columns:
--   id: INTEGER NOT NULL (PRIMARY KEY)
--   email: VARCHAR(120) NOT NULL
--   password_hash: VARCHAR(255) NOT NULL
--   full_name: VARCHAR(100) NOT NULL
--   phone: VARCHAR(15)
--   role: VARCHAR(20) NOT NULL
--   is_active: BOOLEAN
--   created_at: DATETIME

-- ============================================================================
-- SECTION 3: DATA STATISTICS
-- ============================================================================

-- Record counts in each table:
-- consultations: 0 records
-- lawyer_profiles: 0 records
-- legal_acts: 8 records
-- legal_sections: 41 records
-- messages: 0 records
-- users: 3 records

-- ============================================================================
-- SECTION 4: SAMPLE QUERIES
-- ============================================================================

-- Query 1: Display all users
SELECT id, email, full_name, role, is_active FROM users;

-- Results:
-- (1, 'admin@legalconnect.in', 'Admin User', 'admin', 1)
-- (2, 'kabir@gmail.com', 'kabir ', 'lawyer', 1)
-- (3, 'kabir12@gmail.com', 'kabir ', 'customer', 1)

-- Query 2: Display all legal acts
SELECT id, short_name, name, year, category, total_sections FROM legal_acts;

-- Results:
-- (1, 'IPC', 'The Indian Penal Code', 1860, 'Criminal', 511)
-- (2, 'CrPC', 'The Code of Criminal Procedure', 1973, 'Criminal', 484)
-- (3, 'Constitution', 'The Constitution of India', 1950, 'Constitutional', 470)
-- (4, 'Evidence Act', 'The Indian Evidence Act', 1872, 'Civil', 167)
-- (5, 'HMA', 'The Hindu Marriage Act', 1955, 'Family', 30)
-- (6, 'Companies Act', 'The Companies Act', 2013, 'Corporate', 470)
-- (7, 'IT Act', 'The Information Technology Act', 2000, 'Cyber', 94)
-- (8, 'Consumer Act', 'The Consumer Protection Act', 2019, 'Civil', 107)

-- Query 3: Display legal sections with act names (first 10)

        SELECT 
            la.short_name,
            ls.section_number,
            ls.title,
            ls.is_bailable,
            ls.is_cognizable
        FROM legal_sections ls
        JOIN legal_acts la ON ls.act_id = la.id
        LIMIT 10;
        
-- Results:
-- ('IPC', '302', 'Punishment for Murder', 0, 1)
-- ('IPC', '304', 'Punishment for Culpable Homicide Not Amounting to Murder', 1, 0)
-- ('IPC', '307', 'Attempt to Murder', 0, 1)
-- ('IPC', '376', 'Punishment for Rape', 0, 1)
-- ('IPC', '420', 'Cheating and Dishonestly Inducing Delivery of Property', 0, 1)
-- ('IPC', '498A', 'Husband or Relative of Husband Subjecting Woman to Cruelty', 0, 1)
-- ('IPC', '354', 'Assault or Criminal Force to Woman with Intent to Outrage Her Modesty', 0, 1)
-- ('IPC', '375', 'Definition of Rape', 1, 0)
-- ('IPC', '379', 'Punishment for Theft', 1, 1)
-- ('IPC', '406', 'Punishment for Criminal Breach of Trust', 1, 0)

-- Query 4: Count users by role
SELECT role, COUNT(*) as total FROM users GROUP BY role;

-- Results:
-- ('admin', 1)
-- ('customer', 1)
-- ('lawyer', 1)

-- Query 5: Find non-bailable offenses

        SELECT 
            la.short_name,
            ls.section_number,
            ls.title
        FROM legal_sections ls
        JOIN legal_acts la ON ls.act_id = la.id
        WHERE ls.is_bailable = 0;
        
-- Total non-bailable offenses: 6
-- Sample results:
-- ('IPC', '302', 'Punishment for Murder')
-- ('IPC', '307', 'Attempt to Murder')
-- ('IPC', '376', 'Punishment for Rape')
-- ('IPC', '420', 'Cheating and Dishonestly Inducing Delivery of Property')
-- ('IPC', '498A', 'Husband or Relative of Husband Subjecting Woman to Cruelty')

-- ============================================================================
-- SECTION 5: ADVANCED QUERIES (To Impress Evaluator)
-- ============================================================================

-- Query 6: Complete database statistics

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
        
-- Results:
-- ('users', 3)
-- ('lawyer_profiles', 0)
-- ('consultations', 0)
-- ('messages', 0)
-- ('legal_acts', 8)
-- ('legal_sections', 41)

-- Query 7: Group legal acts by category

        SELECT 
            category,
            COUNT(*) as total_acts,
            SUM(total_sections) as total_sections
        FROM legal_acts
        GROUP BY category;
        
-- Results:
-- ('Civil', 2, 274)
-- ('Constitutional', 1, 470)
-- ('Corporate', 1, 470)
-- ('Criminal', 2, 995)
-- ('Cyber', 1, 94)
-- ('Family', 1, 30)

-- ============================================================================
-- SECTION 6: SAMPLE DATA (First 5 records from each table)
-- ============================================================================

-- Sample data from consultations:
-- (No data)

-- Sample data from lawyer_profiles:
-- (No data)

-- Sample data from legal_acts:
-- Columns: id, name, short_name, year, category, description, total_sections, created_at
-- (1, 'The Indian Penal Code', 'IPC', 1860, 'Criminal', 'The main criminal code of India that covers all substantive aspects of criminal law. It defines various crimes and prescribes punishments for them.', 511, '2026-01-30 13:13:52.250307')
-- (2, 'The Code of Criminal Procedure', 'CrPC', 1973, 'Criminal', 'The procedural law for administration of criminal law in India. It provides the machinery for the investigation of crime, apprehension of suspected criminals, collection of evidence, determination of guilt or innocence of the accused person and the determination of punishment.', 484, '2026-01-30 13:13:52.255741')
-- (3, 'The Constitution of India', 'Constitution', 1950, 'Constitutional', 'The supreme law of India. It lays down the framework that demarcates fundamental political code, structure, procedures, powers, and duties of government institutions and sets out fundamental rights, directive principles, and the duties of citizens.', 470, '2026-01-30 13:13:52.263897')
-- (4, 'The Indian Evidence Act', 'Evidence Act', 1872, 'Civil', 'An Act to consolidate, define and amend the law of Evidence. It deals with the rules and principles regarding the admissibility of evidence in courts of law.', 167, '2026-01-30 13:13:52.267361')
-- (5, 'The Hindu Marriage Act', 'HMA', 1955, 'Family', 'An Act to amend and codify the law relating to marriage among Hindus. It deals with marriage, divorce, judicial separation, restitution of conjugal rights, and other matrimonial matters.', 30, '2026-01-30 13:13:52.269698')

-- Sample data from legal_sections:
-- Columns: id, act_id, section_number, title, description, keywords, created_at, penalty, is_bailable, is_cognizable, is_compoundable
-- (1, 1, '302', 'Punishment for Murder', 'Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.', 'murder, death penalty, life imprisonment, homicide, killing, killed, murderer, culpable homicide, intentional killing, death, dead', '2026-01-30 13:13:52.258728', 'Death penalty or life imprisonment and fine', 0, 1, 0)
-- (2, 1, '304', 'Punishment for Culpable Homicide Not Amounting to Murder', 'Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.', 'culpable homicide, manslaughter, unintentional killing', '2026-01-30 13:13:52.258733', None, 1, 0, 0)
-- (3, 1, '307', 'Attempt to Murder', 'Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.', 'attempt to murder, attempted homicide, intention to kill, tried to kill, attack, assault, life-threatening, weapon attack', '2026-01-30 13:13:52.258737', 'Imprisonment up to 10 years and fine', 0, 1, 0)
-- (4, 1, '376', 'Punishment for Rape', 'Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life, and shall also be liable to fine.', 'rape, sexual assault, sexual violence, women safety, forced intercourse, sexual abuse', '2026-01-30 13:13:52.258740', 'Rigorous imprisonment minimum 10 years, may extend to life imprisonment and fine', 0, 1, 0)
-- (5, 1, '420', 'Cheating and Dishonestly Inducing Delivery of Property', 'Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.', 'cheating, fraud, dishonesty, deception, property, cheat, cheated, fraudulent, scam, conned, tricked, deceived, fake, counterfeit, forgery, false promise', '2026-01-30 13:13:52.258742', 'Imprisonment up to 7 years and fine', 0, 1, 0)

-- Sample data from messages:
-- (No data)

-- Sample data from users:
-- Columns: id, email, password_hash, full_name, phone, role, is_active, created_at
-- (1, 'admin@legalconnect.in', 'scrypt:32768:8:1$PgJF29Sr8HFnVXYJ$5d7b87dcb1b5c650a588705aa14acc7fd27bfcb7df7292bfedc90b35dd378fc18934169806360fbd728366145a6c345a7cce9f634c6462a604a2f5370add05fa', 'Admin User', '+91 9999999999', 'admin', 1, '2026-01-25 10:07:36.043037')
-- (2, 'kabir@gmail.com', 'scrypt:32768:8:1$CCzGrpUZtES8iMhm$ed6027e49597171a22876f3ba2c6e02d20d71d0d22c1718f191238e75781d3788437b36a03d3343930bc03c5de6b26bd7fceffdeb6e4124db2e1f5faf270c5a9', 'kabir ', '67876678866', 'lawyer', 1, '2026-01-30 12:53:48.566803')
-- (3, 'kabir12@gmail.com', 'scrypt:32768:8:1$e9akGGIkFH0GJXSN$0b9bd270907b4e103ff86f371b757337c57a0b17cb5e4979adfc4a5590551a29d52c36c13d78f43bc8576d5680060f36f4d454def8320ecdc9228ae62466f908', 'kabir ', '67876678866', 'customer', 1, '2026-01-30 12:56:35.500558')

-- ============================================================================
-- END OF DEMONSTRATION
-- ============================================================================
