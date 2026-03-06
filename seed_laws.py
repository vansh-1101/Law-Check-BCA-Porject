"""
Seed script to populate the database with Indian Legal Acts and Sections
Run this script after creating the database tables: python seed_laws.py
"""
from app import create_app, db
from app.models import LegalAct, LegalSection

def seed_laws():
    """Populate database with Indian legal acts and their sections"""
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if LegalAct.query.first():
            print("⚠️  Legal acts already exist in database. Skipping seed.")
            print(f"   Found {LegalAct.query.count()} acts and {LegalSection.query.count()} sections.")
            return
        
        print("🔨 Seeding Indian Legal Acts and Sections...")
        
        # ========== 1. INDIAN PENAL CODE (IPC), 1860 ==========
        ipc = LegalAct(
            name="The Indian Penal Code",
            short_name="IPC",
            year=1860,
            category="Criminal",
            description="The main criminal code of India that covers all substantive aspects of criminal law. It defines various crimes and prescribes punishments for them.",
            total_sections=511
        )
        db.session.add(ipc)
        db.session.flush()  # Get the ID
        
        ipc_sections = [
            LegalSection(
                act_id=ipc.id,
                section_number="302",
                title="Punishment for Murder",
                description="Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.",
                keywords="murder, death penalty, life imprisonment, homicide, killing, killed, murderer, culpable homicide, intentional killing, death, dead",
                penalty="Death penalty or life imprisonment and fine",
                is_bailable=False,
                is_cognizable=True,
                is_compoundable=False
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="304",
                title="Punishment for Culpable Homicide Not Amounting to Murder",
                description="Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.",
                keywords="culpable homicide, manslaughter, unintentional killing"
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="307",
                title="Attempt to Murder",
                description="Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty of murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine.",
                keywords="attempt to murder, attempted homicide, intention to kill, tried to kill, attack, assault, life-threatening, weapon attack",
                penalty="Imprisonment up to 10 years and fine",
                is_bailable=False,
                is_cognizable=True,
                is_compoundable=False
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="376",
                title="Punishment for Rape",
                description="Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life, and shall also be liable to fine.",
                keywords="rape, sexual assault, sexual violence, women safety"
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="420",
                title="Cheating and Dishonestly Inducing Delivery of Property",
                description="Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
                keywords="cheating, fraud, dishonesty, deception, property, cheat, cheated, fraudulent, scam, conned, tricked, deceived, fake, counterfeit, forgery, false promise",
                penalty="Imprisonment up to 7 years and fine",
                is_bailable=False,
                is_cognizable=True,
                is_compoundable=False
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="498A",
                title="Husband or Relative of Husband Subjecting Woman to Cruelty",
                description="Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine.",
                keywords="domestic violence, cruelty, dowry harassment, women protection"
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="354",
                title="Assault or Criminal Force to Woman with Intent to Outrage Her Modesty",
                description="Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty, shall be punished with imprisonment of either description for a term which shall not be less than one year but which may extend to five years, and shall also be liable to fine.",
                keywords="molestation, assault on women, modesty, sexual harassment, touched, groped, inappropriate touch, eve teasing, stalking, harassment",
                penalty="Imprisonment from 1 to 5 years and fine",
                is_bailable=False,
                is_cognizable=True,
                is_compoundable=False
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="375",
                title="Definition of Rape",
                description="A man is said to commit rape if he has sexual intercourse with a woman under circumstances falling under any of the six descriptions: Against her will, Without her consent, With her consent obtained by putting her or any person in whom she is interested in fear of death or hurt, With her consent when the man knows that he is not her husband, With her consent when she is unable to understand the nature and consequences of that to which she gives consent, With or without her consent when she is under eighteen years of age.",
                keywords="rape definition, sexual intercourse, consent, women rights"
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="379",
                title="Punishment for Theft",
                description="Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
                keywords="theft, stealing, larceny, property crime, stole, stolen, took, taking, dishonestly, movable property, without consent, thief, robbed, robbery, phone theft, mobile theft, wallet theft, bag theft, purse theft",
                penalty="Imprisonment up to 3 years, or fine, or both",
                is_bailable=True,
                is_cognizable=True,
                is_compoundable=False
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="323",
                title="Punishment for Voluntarily Causing Hurt",
                description="Whoever, except in the case provided for by section 334, voluntarily causes hurt, shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both.",
                keywords="hurt, assault, beating, physical violence, injury, injured, hit, punch, kick, slap, fight, attacked, violence, bodily harm, bruises, wounds",
                penalty="Imprisonment up to 1 year, or fine up to ₹1000, or both",
                is_bailable=True,
                is_cognizable=False,
                is_compoundable=True
            ),
            LegalSection(
                act_id=ipc.id,
                section_number="406",
                title="Punishment for Criminal Breach of Trust",
                description="Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
                keywords="breach of trust, embezzlement, misappropriation, fiduciary duty"
            ),
        ]
        db.session.add_all(ipc_sections)
        
        # ========== 2. CODE OF CRIMINAL PROCEDURE (CrPC), 1973 ==========
        crpc = LegalAct(
            name="The Code of Criminal Procedure",
            short_name="CrPC",
            year=1973,
            category="Criminal",
            description="The procedural law for administration of criminal law in India. It provides the machinery for the investigation of crime, apprehension of suspected criminals, collection of evidence, determination of guilt or innocence of the accused person and the determination of punishment.",
            total_sections=484
        )
        db.session.add(crpc)
        db.session.flush()
        
        crpc_sections = [
            LegalSection(
                act_id=crpc.id,
                section_number="41",
                title="When Police May Arrest Without Warrant",
                description="Any police officer may without an order from a Magistrate and without a warrant, arrest any person who has been concerned in any cognizable offence, or against whom a reasonable complaint has been made, or credible information has been received.",
                keywords="arrest, police powers, warrant, cognizable offence"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="154",
                title="Information in Cognizable Cases",
                description="Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under his direction, and be read over to the informant; and every such information, whether given in writing or reduced to writing as aforesaid, shall be signed by the person giving it.",
                keywords="FIR, first information report, police complaint, cognizable offence"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="125",
                title="Order for Maintenance of Wives, Children and Parents",
                description="If any person having sufficient means neglects or refuses to maintain his wife, his legitimate or illegitimate minor child, or his legitimate or illegitimate child who has attained majority where such child is unable to maintain itself, or his father or mother unable to maintain himself or herself, a Magistrate may order such person to make a monthly allowance for the maintenance of his wife or such child, father or mother.",
                keywords="maintenance, alimony, wife maintenance, child support, parents support"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="156",
                title="Police Officer's Power to Investigate Cognizable Case",
                description="Any officer in charge of a police station may, without the order of a Magistrate, investigate any cognizable case which a Court having jurisdiction over the local area within the limits of such station would have power to inquire into or try under the provisions of Chapter XIII.",
                keywords="investigation, police investigation, cognizable case"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="161",
                title="Examination of Witnesses by Police",
                description="Any police officer making an investigation may examine orally any person supposed to be acquainted with the facts and circumstances of the case.",
                keywords="witness examination, police interrogation, investigation"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="167",
                title="Procedure When Investigation Cannot Be Completed in Twenty-Four Hours",
                description="Whenever any person is arrested and detained in custody, and it appears that the investigation cannot be completed within the period of twenty-four hours, the officer in charge of the police station shall transmit to the nearest Judicial Magistrate a copy of the entries in the diary.",
                keywords="police custody, remand, detention, judicial custody"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="437",
                title="When Bail May Be Taken in Case of Non-Bailable Offence",
                description="When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail.",
                keywords="bail, non-bailable offence, release on bail"
            ),
            LegalSection(
                act_id=crpc.id,
                section_number="482",
                title="Saving of Inherent Powers of High Court",
                description="Nothing in this Code shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Code, or to prevent abuse of the process of any Court or otherwise to secure the ends of justice.",
                keywords="inherent powers, high court, quashing, justice"
            ),
        ]
        db.session.add_all(crpc_sections)
        
        # ========== 3. CONSTITUTION OF INDIA, 1950 ==========
        constitution = LegalAct(
            name="The Constitution of India",
            short_name="Constitution",
            year=1950,
            category="Constitutional",
            description="The supreme law of India. It lays down the framework that demarcates fundamental political code, structure, procedures, powers, and duties of government institutions and sets out fundamental rights, directive principles, and the duties of citizens.",
            total_sections=470
        )
        db.session.add(constitution)
        db.session.flush()
        
        constitution_sections = [
            LegalSection(
                act_id=constitution.id,
                section_number="14",
                title="Equality Before Law",
                description="The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.",
                keywords="equality, equal protection, fundamental rights, discrimination"
            ),
            LegalSection(
                act_id=constitution.id,
                section_number="19",
                title="Protection of Certain Rights Regarding Freedom of Speech, etc.",
                description="All citizens shall have the right to freedom of speech and expression; to assemble peaceably and without arms; to form associations or unions; to move freely throughout the territory of India; to reside and settle in any part of the territory of India; and to practise any profession, or to carry on any occupation, trade or business.",
                keywords="freedom of speech, expression, assembly, association, movement, fundamental rights"
            ),
            LegalSection(
                act_id=constitution.id,
                section_number="21",
                title="Protection of Life and Personal Liberty",
                description="No person shall be deprived of his life or personal liberty except according to procedure established by law.",
                keywords="right to life, personal liberty, fundamental rights, due process"
            ),
            LegalSection(
                act_id=constitution.id,
                section_number="32",
                title="Remedies for Enforcement of Rights Conferred by This Part",
                description="The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed.",
                keywords="writ petition, supreme court, enforcement of rights, constitutional remedies"
            ),
            LegalSection(
                act_id=constitution.id,
                section_number="226",
                title="Power of High Courts to Issue Certain Writs",
                description="Notwithstanding anything in Article 32, every High Court shall have power, throughout the territories in relation to which it exercises jurisdiction, to issue to any person or authority, including in appropriate cases, any Government, within those territories directions, orders or writs.",
                keywords="writ jurisdiction, high court, habeas corpus, mandamus, certiorari"
            ),
            LegalSection(
                act_id=constitution.id,
                section_number="356",
                title="Provisions in Case of Failure of Constitutional Machinery in States",
                description="If the President, on receipt of a report from the Governor of a State or otherwise, is satisfied that a situation has arisen in which the government of the State cannot be carried on in accordance with the provisions of this Constitution, the President may by Proclamation assume to himself all or any of the functions of the Government of the State.",
                keywords="president's rule, emergency, state government, constitutional machinery"
            ),
        ]
        db.session.add_all(constitution_sections)
        
        # ========== 4. INDIAN EVIDENCE ACT, 1872 ==========
        evidence_act = LegalAct(
            name="The Indian Evidence Act",
            short_name="Evidence Act",
            year=1872,
            category="Civil",
            description="An Act to consolidate, define and amend the law of Evidence. It deals with the rules and principles regarding the admissibility of evidence in courts of law.",
            total_sections=167
        )
        db.session.add(evidence_act)
        db.session.flush()
        
        evidence_sections = [
            LegalSection(
                act_id=evidence_act.id,
                section_number="3",
                title="Interpretation Clause",
                description="In this Act the following words and expressions are used in the following senses, unless a contrary intention appears from the context: 'Court', 'Fact', 'Relevant', 'Facts in issue', 'Document', 'Evidence', 'Proved', 'Disproved', 'Not proved'.",
                keywords="definitions, interpretation, evidence, court, fact"
            ),
            LegalSection(
                act_id=evidence_act.id,
                section_number="45",
                title="Opinions of Experts",
                description="When the Court has to form an opinion upon a point of foreign law, or of science or art, or as to identity of handwriting or finger impressions, the opinions upon that point of persons specially skilled in such foreign law, science or art, or in questions as to identity of handwriting or finger impressions are relevant facts.",
                keywords="expert opinion, expert witness, scientific evidence, handwriting, fingerprints"
            ),
            LegalSection(
                act_id=evidence_act.id,
                section_number="65B",
                title="Admissibility of Electronic Records",
                description="Notwithstanding anything contained in this Act, any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media produced by a computer shall be deemed to be also a document, if the conditions mentioned in this section are satisfied.",
                keywords="electronic evidence, digital evidence, computer records, cyber law"
            ),
            LegalSection(
                act_id=evidence_act.id,
                section_number="118",
                title="Who May Testify",
                description="All persons shall be competent to testify unless the Court considers that they are prevented from understanding the questions put to them, or from giving rational answers to those questions, by tender years, extreme old age, disease, whether of body or mind, or any other cause of the same kind.",
                keywords="witness competency, testimony, court witness"
            ),
        ]
        db.session.add_all(evidence_sections)
        
        # ========== 5. HINDU MARRIAGE ACT, 1955 ==========
        hindu_marriage = LegalAct(
            name="The Hindu Marriage Act",
            short_name="HMA",
            year=1955,
            category="Family",
            description="An Act to amend and codify the law relating to marriage among Hindus. It deals with marriage, divorce, judicial separation, restitution of conjugal rights, and other matrimonial matters.",
            total_sections=30
        )
        db.session.add(hindu_marriage)
        db.session.flush()
        
        hindu_marriage_sections = [
            LegalSection(
                act_id=hindu_marriage.id,
                section_number="5",
                title="Conditions for a Hindu Marriage",
                description="A marriage may be solemnized between any two Hindus, if the following conditions are fulfilled: (i) neither party has a spouse living at the time of the marriage; (ii) at the time of the marriage, neither party is incapable of giving a valid consent; (iii) the bridegroom has completed the age of twenty-one years and the bride the age of eighteen years; (iv) the parties are not within the degrees of prohibited relationship.",
                keywords="marriage conditions, hindu marriage, valid marriage, age of marriage"
            ),
            LegalSection(
                act_id=hindu_marriage.id,
                section_number="13",
                title="Divorce",
                description="Any marriage solemnized, whether before or after the commencement of this Act, may, on a petition presented by either the husband or the wife, be dissolved by a decree of divorce on various grounds including adultery, cruelty, desertion, conversion, mental disorder, leprosy, venereal disease, renunciation of the world, and presumption of death.",
                keywords="divorce, grounds for divorce, dissolution of marriage, matrimonial relief"
            ),
            LegalSection(
                act_id=hindu_marriage.id,
                section_number="24",
                title="Maintenance Pendente Lite and Expenses of Proceedings",
                description="Where in any proceeding under this Act it appears to the court that either the wife or the husband, as the case may be, has no independent income sufficient for her or his support and the necessary expenses of the proceeding, it may, on the application of the wife or the husband, order the respondent to pay to the petitioner the expenses of the proceeding, and monthly during the proceeding such sum as, having regard to the petitioner's own income and the income of the respondent, it may seem to the court to be reasonable.",
                keywords="interim maintenance, pendente lite, litigation expenses, spousal support"
            ),
            LegalSection(
                act_id=hindu_marriage.id,
                section_number="25",
                title="Permanent Alimony and Maintenance",
                description="Any court exercising jurisdiction under this Act may, at the time of passing any decree or at any time subsequent thereto, on application made to it for the purpose by either the wife or the husband, as the case may be, order that the respondent shall pay to the applicant for her or his maintenance and support such gross sum or such monthly or periodical sum for a term not exceeding the life of the applicant as, having regard to the respondent's own income and other property, if any, the income and other property of the applicant, the conduct of the parties and other circumstances of the case, it may seem to the court to be just.",
                keywords="permanent alimony, maintenance, spousal support, financial support"
            ),
        ]
        db.session.add_all(hindu_marriage_sections)
        
        # ========== 6. COMPANIES ACT, 2013 ==========
        companies_act = LegalAct(
            name="The Companies Act",
            short_name="Companies Act",
            year=2013,
            category="Corporate",
            description="An Act to consolidate and amend the law relating to companies. It deals with incorporation, management, governance, and winding up of companies.",
            total_sections=470
        )
        db.session.add(companies_act)
        db.session.flush()
        
        companies_sections = [
            LegalSection(
                act_id=companies_act.id,
                section_number="7",
                title="Incorporation of Company",
                description="A company may be formed for any lawful purpose by seven or more persons, where the company to be formed is to be a public company, or by two or more persons, where the company to be formed is to be a private company, by subscribing their names to a memorandum and complying with the requirements of this Act in respect of registration.",
                keywords="incorporation, company formation, registration, memorandum"
            ),
            LegalSection(
                act_id=companies_act.id,
                section_number="149",
                title="Company to Have Board of Directors",
                description="Every company shall have a Board of Directors consisting of individuals as directors and shall have a minimum number of three directors in the case of a public company, two directors in the case of a private company, and one director in the case of a One Person Company.",
                keywords="board of directors, directors, corporate governance"
            ),
            LegalSection(
                act_id=companies_act.id,
                section_number="447",
                title="Punishment for Fraud",
                description="Without prejudice to any liability including repayment of any debt under this Act or any other law for the time being in force, any person who is found to be guilty of fraud, shall be punishable with imprisonment for a term which shall not be less than six months but which may extend to ten years and shall also be liable to fine which shall not be less than the amount involved in the fraud, but which may extend to three times the amount involved in the fraud.",
                keywords="corporate fraud, punishment, white collar crime, financial fraud"
            ),
        ]
        db.session.add_all(companies_sections)
        
        # ========== 7. INFORMATION TECHNOLOGY ACT, 2000 ==========
        it_act = LegalAct(
            name="The Information Technology Act",
            short_name="IT Act",
            year=2000,
            category="Cyber",
            description="An Act to provide legal recognition for transactions carried out by means of electronic data interchange and other means of electronic communication, and to facilitate electronic filing of documents with the Government agencies.",
            total_sections=94
        )
        db.session.add(it_act)
        db.session.flush()
        
        it_sections = [
            LegalSection(
                act_id=it_act.id,
                section_number="43",
                title="Penalty and Compensation for Damage to Computer, Computer System, etc.",
                description="If any person without permission of the owner or any other person who is in charge of a computer, computer system or computer network accesses or secures access to such computer, computer system or computer network or downloads, copies or extracts any data, computer data base or information from such computer, he shall be liable to pay damages by way of compensation to the person so affected.",
                keywords="hacking, unauthorized access, cyber crime, data theft, computer damage"
            ),
            LegalSection(
                act_id=it_act.id,
                section_number="66",
                title="Computer Related Offences",
                description="If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both.",
                keywords="cyber crime, hacking punishment, computer offences"
            ),
            LegalSection(
                act_id=it_act.id,
                section_number="66A",
                title="Punishment for Sending Offensive Messages Through Communication Service, etc.",
                description="Any person who sends, by means of a computer resource or a communication device, any information that is grossly offensive or has menacing character; or any information which he knows to be false, but for the purpose of causing annoyance, inconvenience, danger, obstruction, insult, injury, criminal intimidation, enmity, hatred or ill will, persistently by making use of such computer resource or a communication device, shall be punishable with imprisonment for a term which may extend to three years and with fine.",
                keywords="offensive messages, cyber bullying, online harassment, social media crime"
            ),
            LegalSection(
                act_id=it_act.id,
                section_number="67",
                title="Punishment for Publishing or Transmitting Obscene Material in Electronic Form",
                description="Whoever publishes or transmits or causes to be published or transmitted in the electronic form any material which is lascivious or appeals to the prurient interest or if its effect is such as to tend to deprave and corrupt persons who are likely to read, see or hear the matter contained or embodied in it, shall be punished on first conviction with imprisonment of either description for a term which may extend to three years and with fine which may extend to five lakh rupees.",
                keywords="obscene content, pornography, electronic publication, cyber crime"
            ),
        ]
        db.session.add_all(it_sections)
        
        # ========== 8. CONSUMER PROTECTION ACT, 2019 ==========
        consumer_act = LegalAct(
            name="The Consumer Protection Act",
            short_name="Consumer Act",
            year=2019,
            category="Civil",
            description="An Act to provide for protection of the interests of consumers and for the said purpose, to establish authorities for timely and effective administration and settlement of consumers' disputes.",
            total_sections=107
        )
        db.session.add(consumer_act)
        db.session.flush()
        
        consumer_sections = [
            LegalSection(
                act_id=consumer_act.id,
                section_number="2",
                title="Definitions",
                description="In this Act, unless the context otherwise requires: 'consumer' means any person who buys any goods for a consideration or hires or avails of any service for a consideration; 'defect' means any fault, imperfection or shortcoming in the quality, quantity, potency, purity or standard; 'deficiency' means any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance.",
                keywords="consumer definition, defect, deficiency, consumer rights"
            ),
            LegalSection(
                act_id=consumer_act.id,
                section_number="35",
                title="Jurisdiction of District Commission",
                description="Subject to the other provisions of this Act, the District Commission shall have jurisdiction to entertain complaints where the value of the goods or services and the compensation, if any, claimed does not exceed rupees one crore.",
                keywords="district commission, jurisdiction, consumer complaint, compensation"
            ),
        ]
        db.session.add_all(consumer_sections)
        
        # Commit all changes
        db.session.commit()
        
        # Print summary
        total_acts = LegalAct.query.count()
        total_sections = LegalSection.query.count()
        
        print(f"✅ Successfully seeded {total_acts} legal acts and {total_sections} sections!")
        print("\n📊 Summary:")
        for act in LegalAct.query.all():
            section_count = act.sections.count()
            print(f"   • {act.short_name} ({act.year}) - {section_count} sections [{act.category}]")
        
        print("\n🎉 Database seeding complete! You can now browse Indian laws on the website.")


if __name__ == '__main__':
    seed_laws()
