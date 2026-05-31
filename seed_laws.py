"""
Seed script for Indian Legal Acts and Sections
Run:  python seed_laws.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import LegalAct, LegalSection

app = create_app()

ACTS = [
    {"name": "Indian Penal Code", "short_name": "IPC", "year": 1860, "category": "Criminal",
     "description": "The main criminal code of India covering all substantive aspects of criminal law."},
    {"name": "Code of Criminal Procedure", "short_name": "CrPC", "year": 1973, "category": "Criminal",
     "description": "Procedural law for administration of substantive criminal law in India."},
    {"name": "Indian Contract Act", "short_name": "ICA", "year": 1872, "category": "Civil",
     "description": "Governs the law relating to contracts in India."},
    {"name": "Protection of Women from Domestic Violence Act", "short_name": "PWDVA", "year": 2005, "category": "Criminal",
     "description": "Provides protection to women from domestic violence."},
    {"name": "Information Technology Act", "short_name": "IT Act", "year": 2000, "category": "Cyber",
     "description": "Deals with cybercrime and electronic commerce in India."},
    {"name": "Motor Vehicles Act", "short_name": "MVA", "year": 1988, "category": "Civil",
     "description": "Governs all aspects of road transport vehicles in India."},
    {"name": "Consumer Protection Act", "short_name": "CPA", "year": 2019, "category": "Civil",
     "description": "Protects consumer rights and provides remedies for unfair trade practices."},
    {"name": "Hindu Marriage Act", "short_name": "HMA", "year": 1955, "category": "Family",
     "description": "Codifies the law relating to marriage among Hindus."},
    {"name": "Protection of Children from Sexual Offences Act", "short_name": "POCSO", "year": 2012, "category": "Criminal",
     "description": "Protects children from sexual abuse and exploitation."},
    {"name": "Negotiable Instruments Act", "short_name": "NI Act", "year": 1881, "category": "Civil",
     "description": "Deals with promissory notes, bills of exchange and cheques."},
    {"name": "Dowry Prohibition Act", "short_name": "DPA", "year": 1961, "category": "Criminal",
     "description": "Prohibits the giving or taking of dowry."},
    {"name": "SC/ST Prevention of Atrocities Act", "short_name": "SC/ST Act", "year": 1989, "category": "Criminal",
     "description": "Prevents atrocities against Scheduled Castes and Scheduled Tribes."},
    {"name": "Narcotic Drugs and Psychotropic Substances Act", "short_name": "NDPS", "year": 1985, "category": "Criminal",
     "description": "Controls operations relating to narcotic drugs and psychotropic substances."},
    {"name": "Arms Act", "short_name": "Arms Act", "year": 1959, "category": "Criminal",
     "description": "Governs the manufacture, sale, possession and carrying of firearms."},
]

SECTIONS = [
    # === IPC - Murder & Homicide ===
    {"act": "IPC", "section_number": "302", "title": "Punishment for murder",
     "description": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
     "keywords": "murder, kill, killed, killing, death, homicide, stabbed, shot, poisoned, strangled, beat to death, murdered",
     "penalty": "Death penalty or life imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "304", "title": "Culpable homicide not amounting to murder",
     "description": "Whoever commits culpable homicide not amounting to murder shall be punished with imprisonment for life, or imprisonment up to 10 years, and fine.",
     "keywords": "culpable homicide, manslaughter, accidental death, unintentional killing, negligent death",
     "penalty": "Life imprisonment or up to 10 years and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "304A", "title": "Causing death by negligence",
     "description": "Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide.",
     "keywords": "death by negligence, rash driving death, accidental death, road accident death, medical negligence death",
     "penalty": "Up to 2 years imprisonment or fine or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "304B", "title": "Dowry death",
     "description": "Where the death of a woman is caused by burns or bodily injury within 7 years of marriage, and she was subjected to cruelty for dowry.",
     "keywords": "dowry death, bride burning, wife killed for dowry, burned alive, dowry murder",
     "penalty": "Not less than 7 years, may extend to life imprisonment", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Attempt to Murder
    {"act": "IPC", "section_number": "307", "title": "Attempt to murder",
     "description": "Whoever does any act with the intention or knowledge that he would cause death.",
     "keywords": "attempt to murder, tried to kill, attempted murder, attack with weapon, stabbing, shooting, poisoning attempt",
     "penalty": "Up to 10 years and fine; if hurt caused, life imprisonment", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Hurt
    {"act": "IPC", "section_number": "323", "title": "Voluntarily causing hurt",
     "description": "Whoever voluntarily causes hurt shall be punished with imprisonment up to one year, or fine, or both.",
     "keywords": "hurt, hit, slap, punch, beat, beating, assault, attacked, pushed, kicked, injured, violence, fight, fighting, beaten, physical attack",
     "penalty": "Up to 1 year imprisonment or fine up to Rs.1000 or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IPC", "section_number": "325", "title": "Voluntarily causing grievous hurt",
     "description": "Whoever voluntarily causes grievous hurt shall be punished with imprisonment up to seven years and fine.",
     "keywords": "grievous hurt, serious injury, broken bone, fracture, permanent damage, severe beating, serious assault, badly injured",
     "penalty": "Up to 7 years imprisonment and fine", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IPC", "section_number": "326", "title": "Grievous hurt by dangerous weapons",
     "description": "Whoever voluntarily causes grievous hurt by means of any instrument for shooting, stabbing or cutting.",
     "keywords": "acid attack, knife attack, dangerous weapon, sword, blade, weapon, acid, burning, sharp weapon, iron rod",
     "penalty": "Life imprisonment or up to 10 years and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Assault
    {"act": "IPC", "section_number": "352", "title": "Assault or criminal force",
     "description": "Whoever assaults or uses criminal force to any person otherwise than on grave and sudden provocation.",
     "keywords": "assault, criminal force, pushed, shoved, grabbed, manhandled, physical force, aggression",
     "penalty": "Up to 3 months imprisonment or fine up to Rs.500 or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Kidnapping
    {"act": "IPC", "section_number": "363", "title": "Punishment for kidnapping",
     "description": "Whoever kidnaps any person from India or from lawful guardianship.",
     "keywords": "kidnap, kidnapping, kidnapped, abduction, abducted, taken away, missing child, child stolen, snatched child, forcibly taken",
     "penalty": "Up to 7 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "364A", "title": "Kidnapping for ransom",
     "description": "Whoever kidnaps or abducts any person and threatens to cause death or hurt, and demands ransom.",
     "keywords": "kidnap for ransom, ransom, hostage, ransom demand, kidnapped for money",
     "penalty": "Death or life imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Rape & Sexual Offences
    {"act": "IPC", "section_number": "376", "title": "Punishment for rape",
     "description": "Whoever commits rape shall be punished with rigorous imprisonment for not less than ten years, extendable to life imprisonment, and fine.",
     "keywords": "rape, raped, rapped, sexual assault, sexual violence, forced sex, molestation, sexually assaulted, molested, sexual abuse, violated sexually, forced intercourse, ravished",
     "penalty": "Not less than 10 years rigorous imprisonment, may extend to life, and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "376D", "title": "Gang rape",
     "description": "Where a woman is raped by one or more persons constituting a group or acting in furtherance of common intention.",
     "keywords": "gang rape, group rape, gangrape, multiple persons rape",
     "penalty": "Not less than 20 years rigorous imprisonment to life and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "354", "title": "Assault on woman to outrage her modesty",
     "description": "Whoever assaults or uses criminal force to any woman, intending to outrage her modesty.",
     "keywords": "eve teasing, molestation, molested, groping, touching inappropriately, outrage modesty, indecent touch, sexual harassment physical",
     "penalty": "1 to 5 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "354A", "title": "Sexual harassment",
     "description": "Physical contact and advances involving unwelcome and explicit sexual overtures, demand for sexual favours, showing pornography.",
     "keywords": "sexual harassment, inappropriate advances, unwelcome touch, sexual comments, workplace harassment, sexual favours demand, obscene remarks",
     "penalty": "Up to 3 years imprisonment and/or fine", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "354D", "title": "Stalking",
     "description": "Any man who follows a woman and contacts or attempts to contact despite clear indication of disinterest.",
     "keywords": "stalking, stalker, following, monitoring, tracking, watching, harassing, following repeatedly, cyber stalking, online stalking",
     "penalty": "Up to 3 years on first conviction, up to 5 years on subsequent", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    # Theft & Robbery
    {"act": "IPC", "section_number": "379", "title": "Punishment for theft",
     "description": "Whoever commits theft shall be punished with imprisonment up to three years, or fine, or both.",
     "keywords": "theft, steal, stolen, stole, robbed, pickpocket, shoplifting, burglary, phone stolen, wallet stolen, snatching, bag snatching, mobile stolen, chain snatching, thief",
     "penalty": "Up to 3 years imprisonment or fine or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "392", "title": "Punishment for robbery",
     "description": "Whoever commits robbery shall be punished with rigorous imprisonment up to ten years and fine.",
     "keywords": "robbery, armed robbery, loot, looting, gunpoint, knifepoint, mugging, mugged, snatching with force, dacoity",
     "penalty": "Up to 10 years rigorous imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # House Breaking
    {"act": "IPC", "section_number": "454", "title": "House-breaking to commit offence",
     "description": "Whoever commits lurking house-trespass or house-breaking in order to commit any offence punishable with imprisonment.",
     "keywords": "house breaking, break in, broke into house, burglary, home invasion, intruder, someone entered my house",
     "penalty": "Up to 3 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Cheating & Fraud
    {"act": "IPC", "section_number": "420", "title": "Cheating and dishonestly inducing delivery of property",
     "description": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property.",
     "keywords": "cheating, fraud, scam, scammed, cheated, deceived, fake product, duplicate, con, swindled, fraudulent, tricked, duped, forgery, fake, counterfeit, investment fraud, online fraud, money fraud",
     "penalty": "Up to 7 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "406", "title": "Criminal breach of trust",
     "description": "Whoever commits criminal breach of trust shall be punished with imprisonment up to three years, or fine, or both.",
     "keywords": "breach of trust, misappropriation, embezzlement, money not returned, betrayal of trust, funds misused",
     "penalty": "Up to 3 years imprisonment or fine or both", "is_bailable": False, "is_cognizable": True, "is_compoundable": True},
    # Extortion & Blackmail
    {"act": "IPC", "section_number": "383", "title": "Extortion",
     "description": "Whoever intentionally puts any person in fear of injury and thereby dishonestly induces delivery of property.",
     "keywords": "extortion, blackmail, threatening for money, demanding money threats, ransom, threatened, protection money",
     "penalty": "Up to 3 years imprisonment or fine or both", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Intimidation
    {"act": "IPC", "section_number": "506", "title": "Criminal intimidation",
     "description": "Whoever commits criminal intimidation shall be punished. If threat is to cause death or grievous hurt, up to 7 years.",
     "keywords": "threatening, threat, intimidation, death threat, threatened to kill, life threat, threatened, menacing, scared, fear, terrorizing, threatening messages, threatening call",
     "penalty": "Up to 2 years or fine or both; up to 7 years if threat of death", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Defamation
    {"act": "IPC", "section_number": "499", "title": "Defamation",
     "description": "Whoever makes or publishes any imputation concerning any person intending to harm reputation.",
     "keywords": "defamation, slander, character assassination, false accusation, spreading rumors, reputation damage, libel, fake news about me, false statement",
     "penalty": "Up to 2 years imprisonment or fine or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Cruelty / Domestic Violence
    {"act": "IPC", "section_number": "498A", "title": "Cruelty by husband or relatives",
     "description": "Whoever, being the husband or relative of husband, subjects a woman to cruelty shall be punished.",
     "keywords": "dowry harassment, cruelty by husband, domestic violence, wife beating, marital abuse, mental cruelty, in-laws harassment, husband torture, dowry demand, harassed by husband, beaten by husband, abused by husband",
     "penalty": "Up to 3 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Property
    {"act": "IPC", "section_number": "447", "title": "Criminal trespass",
     "description": "Whoever commits criminal trespass shall be punished with imprisonment up to three months, or fine, or both.",
     "keywords": "trespass, encroachment, occupied my land, illegal occupation, land grabbing, land dispute, entered my property, illegal entry, squatter, property dispute",
     "penalty": "Up to 3 months imprisonment or fine up to Rs.500 or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Mischief
    {"act": "IPC", "section_number": "425", "title": "Mischief - Property damage",
     "description": "Whoever destroys or diminishes the value or utility of any property, or damages it.",
     "keywords": "property damage, vandalism, destroyed property, damaged car, broken window, arson, fire, set fire, destruction of property",
     "penalty": "Up to 3 months imprisonment or fine or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Forgery
    {"act": "IPC", "section_number": "468", "title": "Forgery for purpose of cheating",
     "description": "Whoever commits forgery intending that the document forged shall be used for cheating.",
     "keywords": "forgery, forged document, fake document, forged signature, fake certificate, false document, document fraud, forged cheque",
     "penalty": "Up to 7 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # Rioting
    {"act": "IPC", "section_number": "147", "title": "Punishment for rioting",
     "description": "Whoever is guilty of rioting shall be punished with imprisonment up to two years or fine or both.",
     "keywords": "rioting, riot, mob violence, mob attack, group violence, public disturbance, violent protest",
     "penalty": "Up to 2 years imprisonment or fine or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    # Wrongful Restraint
    {"act": "IPC", "section_number": "341", "title": "Wrongful restraint",
     "description": "Whoever wrongfully restrains any person shall be punished.",
     "keywords": "wrongful restraint, detained illegally, false imprisonment, locked in room, held against will, confined, restrained",
     "penalty": "Up to 1 month imprisonment or fine up to Rs.500 or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # Obscene acts
    {"act": "IPC", "section_number": "509", "title": "Word, gesture or act to insult modesty of woman",
     "description": "Whoever intending to insult the modesty of any woman utters any word, makes any sound or gesture.",
     "keywords": "obscene gestures, verbal abuse women, cat calling, vulgar comments, insulting woman, indecent remarks, lewd comments",
     "penalty": "Up to 3 years imprisonment and fine", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    {"act": "IPC", "section_number": "279", "title": "Rash driving on public way",
     "description": "Whoever drives any vehicle on any public way in a manner so rash or negligent as to endanger human life.",
     "keywords": "rash driving, negligent driving, dangerous driving, reckless driving, speeding, wrong side driving",
     "penalty": "Up to 6 months imprisonment or fine up to Rs.1000 or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    # === PWDVA ===
    {"act": "PWDVA", "section_number": "3", "title": "Definition of domestic violence",
     "description": "Any act of physical, sexual, verbal, emotional and economic abuse by the respondent against the aggrieved person.",
     "keywords": "domestic violence, wife abuse, beaten by husband, marital abuse, physical abuse home, emotional abuse, verbal abuse, family violence, abusive husband, abusive partner",
     "penalty": "Protection orders, residence orders, monetary relief, custody orders", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    {"act": "PWDVA", "section_number": "18", "title": "Protection orders",
     "description": "The Magistrate may pass a protection order prohibiting the respondent from committing any act of domestic violence.",
     "keywords": "protection order, restraining order, stay away order, domestic violence protection, safety order",
     "penalty": "Breach: up to 1 year imprisonment and/or fine up to Rs.20000", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === IT ACT ===
    {"act": "IT Act", "section_number": "66", "title": "Computer related offences",
     "description": "If any person dishonestly or fraudulently does any act referred to in section 43 he shall be punishable.",
     "keywords": "hacking, computer fraud, unauthorized access, data theft, cyber crime, system hacking, computer tampering, digital fraud",
     "penalty": "Up to 3 years imprisonment or fine up to Rs.5 lakh or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IT Act", "section_number": "66C", "title": "Identity theft",
     "description": "Whoever fraudulently uses the electronic signature, password or unique identification of another person.",
     "keywords": "identity theft, password stolen, account hacked, identity fraud, impersonation online, fake profile, phishing, hacked account",
     "penalty": "Up to 3 years imprisonment and fine up to Rs.1 lakh", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IT Act", "section_number": "66D", "title": "Cheating by personation using computer resource",
     "description": "Whoever cheats by personation by using any communication device or computer resource.",
     "keywords": "online fraud, internet scam, fake website fraud, phishing scam, email scam, UPI fraud, online cheating, digital fraud, cyber fraud, bank fraud online, OTP fraud",
     "penalty": "Up to 3 years imprisonment and fine up to Rs.1 lakh", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IT Act", "section_number": "66E", "title": "Violation of privacy",
     "description": "Whoever captures, publishes or transmits the image of a private area of any person without consent.",
     "keywords": "privacy violation, private photos leaked, intimate images shared, revenge porn, morphed photos, leaked photos, voyeurism, private video leaked, MMS leak, nude photos shared",
     "penalty": "Up to 3 years imprisonment or fine up to Rs.2 lakh or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "IT Act", "section_number": "67", "title": "Publishing obscene material electronically",
     "description": "Whoever publishes or transmits obscene material in electronic form.",
     "keywords": "obscene content online, pornography distribution, sharing obscene material, cyber bullying, online threats, abusive messages online, social media threats, online harassment, trolling, cyber harassment",
     "penalty": "Up to 3 years imprisonment and fine up to Rs.5 lakh on first conviction", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    # === MVA ===
    {"act": "MVA", "section_number": "184", "title": "Driving dangerously",
     "description": "Whoever drives a motor vehicle at a speed or in a manner dangerous to the public.",
     "keywords": "rash driving, dangerous driving, overspeeding, reckless driving, drunk driving, hit and run, road accident, car accident, bike accident, vehicle accident",
     "penalty": "Up to 6 months imprisonment or fine up to Rs.1000 or both", "is_bailable": True, "is_cognizable": True, "is_compoundable": True},
    {"act": "MVA", "section_number": "185", "title": "Driving under influence of alcohol/drugs",
     "description": "Whoever drives a motor vehicle while under the influence of alcohol or drugs.",
     "keywords": "drunk driving, driving under influence, DUI, intoxicated driving, alcohol driving",
     "penalty": "Up to 6 months and/or fine up to Rs.10000; repeat: up to 2 years", "is_bailable": True, "is_cognizable": True, "is_compoundable": False},
    # === CPA ===
    {"act": "CPA", "section_number": "2(6)", "title": "Deficiency in service",
     "description": "Any fault, imperfection, shortcoming in the quality of service.",
     "keywords": "bad service, defective product, consumer complaint, product defect, poor service, warranty issue, refund denied, faulty product, consumer rights",
     "penalty": "Compensation, replacement, refund, or repair as ordered by Consumer Forum", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    {"act": "CPA", "section_number": "2(47)", "title": "Unfair trade practice",
     "description": "A trade practice which adopts unfair method or deception for promoting sale of goods or services.",
     "keywords": "unfair trade, misleading advertisement, false advertising, deceptive marketing, hidden charges, overcharging, fake offer, false promise",
     "penalty": "Compensation as decided by Consumer Forum", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # === NI ACT ===
    {"act": "NI Act", "section_number": "138", "title": "Dishonour of cheque",
     "description": "Where any cheque is returned by the bank unpaid due to insufficient funds.",
     "keywords": "cheque bounce, bounced cheque, dishonoured cheque, insufficient funds, cheque returned, bad cheque, check bounce",
     "penalty": "Up to 2 years imprisonment or fine up to twice the cheque amount or both", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    # === DPA ===
    {"act": "DPA", "section_number": "3", "title": "Penalty for giving or taking dowry",
     "description": "If any person gives or takes or abets the giving or taking of dowry he shall be punishable.",
     "keywords": "dowry, dowry demand, dowry harassment, dahej, demanding dowry, giving dowry, taking dowry",
     "penalty": "Not less than 5 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === SC/ST ACT ===
    {"act": "SC/ST Act", "section_number": "3", "title": "Punishments for offences of atrocities",
     "description": "Whoever commits offences against a member of SC/ST including assault, forced labour, insult etc.",
     "keywords": "caste discrimination, untouchability, caste abuse, SC ST harassment, dalit abuse, caste violence, caste atrocity, discrimination",
     "penalty": "6 months to 5 years imprisonment and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === POCSO ===
    {"act": "POCSO", "section_number": "4", "title": "Penetrative sexual assault on child",
     "description": "Whoever commits penetrative sexual assault on a child shall be punished.",
     "keywords": "child abuse, child sexual abuse, child rape, minor abuse, child molestation, minor sexually assaulted, child molested, POCSO",
     "penalty": "Not less than 10 years, may extend to life, and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === NDPS ===
    {"act": "NDPS", "section_number": "20", "title": "Cannabis possession/consumption",
     "description": "Whoever possesses, sells, purchases, transports, or consumes cannabis (ganja, charas, marijuana).",
     "keywords": "drugs, ganja, marijuana, cannabis, charas, weed, drug possession, drug dealing, narcotics, smoking weed",
     "penalty": "Small qty: up to 1 year; Commercial qty: 10-20 years and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    {"act": "NDPS", "section_number": "21", "title": "Manufactured drugs possession",
     "description": "Whoever possesses manufactured drugs like heroin, cocaine, MDMA etc.",
     "keywords": "heroin, cocaine, MDMA, drug abuse, substance abuse, brown sugar, smack, crystal meth",
     "penalty": "Small qty: up to 1 year; Commercial: 10-20 years and fine", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === ARMS ACT ===
    {"act": "Arms Act", "section_number": "25", "title": "Illegal possession of arms",
     "description": "Whoever acquires, possesses, or carries any firearm or ammunition without license.",
     "keywords": "illegal weapon, gun without license, illegal firearm, unlicensed gun, illegal arms, pistol, revolver",
     "penalty": "1 to 3 years for regular firearms; 3 to 7 years for prohibited arms", "is_bailable": False, "is_cognizable": True, "is_compoundable": False},
    # === HMA ===
    {"act": "HMA", "section_number": "13", "title": "Divorce",
     "description": "Either party may present petition for dissolution of marriage on grounds of adultery, cruelty, desertion, etc.",
     "keywords": "divorce, separation, marriage dissolution, adultery, desertion, cruelty marriage, divorce petition, mutual divorce, husband left, wife left",
     "penalty": "Decree of divorce, maintenance, alimony, custody", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
    {"act": "HMA", "section_number": "24", "title": "Maintenance pendente lite",
     "description": "Either spouse may apply for maintenance if having no independent income.",
     "keywords": "maintenance, alimony, spousal support, wife maintenance, husband not giving money, financial support marriage",
     "penalty": "Court-ordered maintenance amount", "is_bailable": True, "is_cognizable": False, "is_compoundable": True},
]

def seed():
    with app.app_context():
        existing = LegalAct.query.count()
        if existing > 0:
            print(f"Database already has {existing} acts. Clearing and re-seeding...")
            LegalSection.query.delete()
            LegalAct.query.delete()
            db.session.commit()

        act_map = {}
        for act_data in ACTS:
            act = LegalAct(**act_data)
            db.session.add(act)
            db.session.flush()
            act_map[act_data["short_name"]] = act
            print(f"  + Act: {act_data['short_name']} ({act_data['name']})")

        count = 0
        for sec_data in SECTIONS:
            act_key = sec_data.pop("act")
            act = act_map.get(act_key)
            if not act:
                print(f"  ! Skipping section {sec_data['section_number']} - act '{act_key}' not found")
                sec_data["act"] = act_key
                continue
            section = LegalSection(act_id=act.id, **sec_data)
            db.session.add(section)
            count += 1
            sec_data["act"] = act_key

        for short_name, act in act_map.items():
            act.total_sections = LegalSection.query.filter_by(act_id=act.id).count()

        db.session.commit()
        print(f"\nSeeded {len(act_map)} acts and {count} sections successfully!")

if __name__ == "__main__":
    seed()
