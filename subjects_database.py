"""
VTU Subjects Database - Comprehensive collection of all VTU courses with credits
This file contains all VTU subjects organized by scheme, semester, and branch
"""

# VTU SUBJECTS DATABASE
VTU_SUBJECTS_DATABASE = {
    # ===== 2022 SCHEME (LATEST) =====
    "2022": {
        "CS": {  # Computer Science & Engineering
            "1": [  # 1st Semester
                {"code": "BMATS101", "name": "MATHEMATICS-I FOR CSE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BPHYS102", "name": "APPLIED PHYSICS FOR CSE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BCHES102", "name": "APPLIED CHEMISTRY FOR CSE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BPOPS103", "name": "PRINCIPLES OF PROGRAMMING USING C", "credits": 3, "type": "ESC"},
                {"code": "BCEDK103", "name": "COMPUTER-AIDED ENGINEERING DRAWING", "credits": 3, "type": "ESC"},
                # Engineering Science Courses-I (ESC-I)
                {"code": "BESCK104A", "name": "INTRODUCTION TO CIVIL ENGINEERING", "credits": 3, "type": "ESC-I"},
                {"code": "BESCK104B", "name": "INTRODUCTION TO ELECTRICAL ENGINEERING", "credits": 3, "type": "ESC-I"},
                {"code": "BESCK104C", "name": "INTRODUCTION TO ELECTRONICS COMMUNICATION", "credits": 3, "type": "ESC-I"},
                {"code": "BESCK104D", "name": "INTRODUCTION TO MECHANICAL ENGINEERING", "credits": 3, "type": "ESC-I"},
                {"code": "BESCK104E", "name": "INTRODUCTION TO C PROGRAMMING", "credits": 3, "type": "ESC-I"},
                # Emerging Technology Course - I (ETC-I)
                {"code": "BETCK105A", "name": "SMART MATERIALS AND SYSTEMS", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105B", "name": "GREEN BUILDINGS", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105C", "name": "INTRODUCTION TO NANO TECHNOLOGY", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105D", "name": "INTRODUCTION TO SUSTAINABLE ENGINEERING", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105E", "name": "RENEWABLE ENERGY SOURCES", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105F", "name": "WASTE MANAGEMENT", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105G", "name": "EMERGING APPLICATIONS OF BIOSENSORS", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105H", "name": "INTRODUCTION TO INTERNET OF THINGS (IOT)", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105I", "name": "INTRODUCTION TO CYBER SECURITY", "credits": 3, "type": "ETC-I"},
                {"code": "BETCK105J", "name": "INTRODUCTION TO EMBEDDED SYSTEM", "credits": 3, "type": "ETC-I"},
                # Programming Language Course - I (PLC-I)
                {"code": "BPLCK105A", "name": "INTRODUCTION TO WEB PROGRAMMING", "credits": 3, "type": "PLC-I"},
                {"code": "BPLCK105B", "name": "INTRODUCTION TO PYTHON PROGRAMMING", "credits": 3, "type": "PLC-I"},
                {"code": "BPLCK105C", "name": "BASICS OF JAVA PROGRAMMING", "credits": 3, "type": "PLC-I"},
                {"code": "BPLCK105D", "name": "INTRODUCTION TO C++ PROGRAMMING", "credits": 3, "type": "PLC-I"},
                # Ability Enhancement Course (AEC)
                {"code": "BENGK106", "name": "COMMUNICATIVE ENGLISH", "credits": 1, "type": "AEC"},
                {"code": "BPWSK106", "name": "PROFESSIONAL WRITING SKILLS IN ENGLISH", "credits": 1, "type": "AEC"},
                # Humanities and Social Management Course (HSMC)
                {"code": "BICOK107", "name": "INDIAN CONSTITUTION", "credits": 1, "type": "HSMC"},
                {"code": "BKSKK107", "name": "SAMSKRUTIKA KANNADA", "credits": 1, "type": "HSMC"},
                {"code": "BKBKK107", "name": "BALAKE KANNADA", "credits": 1, "type": "HSMC"},
                # Skill Development Course (SDC)
                {"code": "BIDTK158", "name": "INNOVATION AND DESIGN THINKING", "credits": 1, "type": "SDC"},
                {"code": "BSFHK158", "name": "SCIENTIFIC FOUNDATIONS OF HEALTH", "credits": 1, "type": "SDC"},
            ],
            "2": [  # 2nd Semester
                {"code": "BMATS201", "name": "MATHEMATICS-II FOR CSE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BCHES202", "name": "APPLIED CHEMISTRY FOR CSE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BCEDK203", "name": "COMPUTER-AIDED ENGINEERING DRAWING", "credits": 3, "type": "ESC"},
                # Engineering Science Courses-II (ESC-II)
                {"code": "BESCK204A", "name": "INTRODUCTION TO CIVIL ENGINEERING", "credits": 3, "type": "ESC-II"},
                {"code": "BESCK204B", "name": "INTRODUCTION TO ELECTRICAL ENGINEERING", "credits": 3, "type": "ESC-II"},
                {"code": "BESCK204C", "name": "INTRODUCTION TO ELECTRONICS COMMUNICATION", "credits": 3, "type": "ESC-II"},
                {"code": "BESCK204D", "name": "INTRODUCTION TO MECHANICAL ENGINEERING", "credits": 3, "type": "ESC-II"},
                {"code": "BESCK204E", "name": "INTRODUCTION TO C PROGRAMMING", "credits": 3, "type": "ESC-II"},
                # Emerging Technology Course - II (ETC-II)
                {"code": "BETCK205A", "name": "SMART MATERIALS AND SYSTEMS", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205B", "name": "GREEN BUILDINGS", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205C", "name": "INTRODUCTION TO NANO TECHNOLOGY", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205D", "name": "INTRODUCTION TO SUSTAINABLE ENGINEERING", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205E", "name": "RENEWABLE ENERGY SOURCES", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205F", "name": "WASTE MANAGEMENT", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205G", "name": "EMERGING APPLICATIONS OF BIOSENSORS", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205H", "name": "INTRODUCTION TO INTERNET OF THINGS (IOT)", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205I", "name": "INTRODUCTION TO CYBER SECURITY", "credits": 3, "type": "ETC-II"},
                {"code": "BETCK205J", "name": "INTRODUCTION TO EMBEDDED SYSTEM", "credits": 3, "type": "ETC-II"},
                # Programming Language Course - II (PLC-II)
                {"code": "BPLCK205A", "name": "INTRODUCTION TO WEB PROGRAMMING", "credits": 3, "type": "PLC-II"},
                {"code": "BPLCK205B", "name": "INTRODUCTION TO PYTHON PROGRAMMING", "credits": 3, "type": "PLC-II"},
                {"code": "BPLCK205C", "name": "BASICS OF JAVA PROGRAMMING", "credits": 3, "type": "PLC-II"},
                {"code": "BPLCK205D", "name": "INTRODUCTION TO C++ PROGRAMMING", "credits": 3, "type": "PLC-II"},
                # Ability Enhancement Course (AEC)
                {"code": "BENGK206", "name": "COMMUNICATIVE ENGLISH", "credits": 1, "type": "AEC"},
                {"code": "BPWSK206", "name": "PROFESSIONAL WRITING SKILLS IN ENGLISH", "credits": 1, "type": "AEC"},
                # Humanities and Social Management Course (HSMS)
                {"code": "BICOK207", "name": "INDIAN CONSTITUTION", "credits": 1, "type": "HSMS"},
                {"code": "BKSKK207", "name": "SAMSKRUTIKA KANNADA", "credits": 1, "type": "HSMS"},
                {"code": "BKBKK207", "name": "BALAKE KANNADA", "credits": 1, "type": "HSMS"},
                # Skill Development Course (SDC)
                {"code": "BIDTK258", "name": "INNOVATION AND DESIGN THINKING", "credits": 1, "type": "SDC"},
                {"code": "BSFHK258", "name": "SCIENTIFIC FOUNDATIONS OF HEALTH", "credits": 1, "type": "SDC"},
            ],
            "3": [  # 3rd Semester (2023-24)
                {"code": "BCS301", "name": "MATHEMATICS FOR COMPUTER SCIENCE", "credits": 4, "type": "PCC"},
                {"code": "BCS302", "name": "DIGITAL DESIGN & COMPUTER ORGANIZATION", "credits": 4, "type": "IPCC"},
                {"code": "BCS303", "name": "OPERATING SYSTEMS", "credits": 4, "type": "IPCC"},
                {"code": "BCS304", "name": "DATA STRUCTURES AND APPLICATIONS", "credits": 3, "type": "PCC"},
                {"code": "BCSL305", "name": "DATA STRUCTURES LAB", "credits": 1, "type": "PCCL"},
                {"code": "BCS306A", "name": "OBJECT ORIENTED PROGRAMMING WITH JAVA", "credits": 3, "type": "ESC/ETC/PLC"},
                {"code": "BCS306B", "name": "OBJECT ORIENTED PROGRAMMING WITH C++", "credits": 3, "type": "ESC/ETC/PLC"},
                {"code": "BSCK307", "name": "SOCIAL CONNECT AND RESPONSIBILITY", "credits": 1, "type": "UHV"},
                # Ability Enhancement Courses / Skill Enhancement Courses
                {"code": "BCSL358A", "name": "DATA ANALYTICS WITH EXCEL", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL358B", "name": "R PROGRAMMING", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL358C", "name": "PROJECT MANAGEMENT WITH GIT", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL358D", "name": "DATA VISUALIZATION WITH PYTHON", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCS358D", "name": "DATA VISUALIZATION WITH PYTHON", "credits": 1, "type": "AEC/SEC"},  # Alternative code from PDF
                # Mandatory / Co-curricular
                {"code": "BNSK359", "name": "NATIONAL SERVICE SCHEME (NSS)", "credits": 0, "type": "MC"},
                {"code": "BPEK359", "name": "PHYSICAL EDUCATION (SPORTS AND ATHLETICS)", "credits": 0, "type": "MC"},
                {"code": "BYOK359", "name": "YOGA", "credits": 0, "type": "MC"},
            ],
            "4": [  # 4th Semester (2023-24)
                {"code": "BCS401", "name": "ANALYSIS & DESIGN OF ALGORITHMS", "credits": 3, "type": "PCC"},
                {"code": "BCS402", "name": "MICROCONTROLLERS", "credits": 4, "type": "IPCC"},
                {"code": "BCS403", "name": "DATABASE MANAGEMENT SYSTEMS", "credits": 4, "type": "IPCC"},
                {"code": "BCSL404", "name": "ANALYSIS & DESIGN OF ALGORITHMS LAB", "credits": 1, "type": "PCCL"},
                {"code": "BBOC407", "name": "BIOLOGY FOR COMPUTER ENGINEERS", "credits": 2, "type": "OE"},
                {"code": "BUHK408", "name": "UNIVERSAL HUMAN VALUES COURSE", "credits": 1, "type": "UHV"},
                {"code": "BCS405A", "name": "DISCRETE MATHEMATICAL STRUCTURES", "credits": 3, "type": "ESC"},
                # Relevant Ability Enhancement Courses
                {"code": "BCS456A", "name": "GREEN IT AND SUSTAINABILITY", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCS456B", "name": "CAPACITY PLANNING FOR IT", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCS456C", "name": "UI/UX", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL456D", "name": "TECHNICAL WRITING USING LATEX", "credits": 1, "type": "AEC/SEC"},
            ],
            "5": [  # 5th Semester
                {"code": "BCS501", "name": "SOFTWARE ENGINEERING & PROJECT MANAGEMENT", "credits": 4, "type": "PCC"},
                {"code": "BCS502", "name": "COMPUTER NETWORKS", "credits": 4, "type": "IPCC"},
                {"code": "BCS503", "name": "THEORY OF COMPUTATION", "credits": 4, "type": "PCC"},
                {"code": "BCSL504", "name": "WEB TECHNOLOGY LAB", "credits": 1, "type": "PCCL"},
                {"code": "BCS515x", "name": "PROFESSIONAL ELECTIVE COURSE", "credits": 3, "type": "PEC"},
                {"code": "BCS586", "name": "MINI PROJECT", "credits": 2, "type": "PROJ"},
                {"code": "BRMK557", "name": "RESEARCH METHODOLOGY AND IPR", "credits": 3, "type": "AEC"},
                {"code": "BCS508", "name": "ENVIRONMENTAL STUDIES AND E-WASTE MANAGEMENT", "credits": 1, "type": "HSMS"},
                {"code": "BNSK559", "name": "NATIONAL SERVICE SCHEME (NSS)", "credits": 0, "type": "MC"},
                {"code": "BPEK559", "name": "PHYSICAL EDUCATION (SPORTS AND ATHLETICS)", "credits": 0, "type": "MC"},
                {"code": "BYOK559", "name": "YOGA", "credits": 0, "type": "MC"},
            ],
            "6": [  # 6th Semester
                {"code": "BCS601", "name": "CLOUD COMPUTING (OPEN STACK / GOOGLE)", "credits": 4, "type": "IPCC"},
                {"code": "BCS602", "name": "MACHINE LEARNING", "credits": 4, "type": "PCC"},
                {"code": "BXX613x", "name": "PROFESSIONAL ELECTIVE COURSE", "credits": 3, "type": "PEC"},
                {"code": "BXX654x", "name": "OPEN ELECTIVE COURSE", "credits": 3, "type": "OEC"},
                {"code": "BCS685", "name": "PROJECT PHASE I", "credits": 2, "type": "PROJ"},
                {"code": "BCSL606", "name": "MACHINE LEARNING LAB", "credits": 1, "type": "PCCL"},
                {"code": "BXX657x", "name": "ABILITY ENHANCEMENT COURSE / SKILL DEVELOPMENT COURSE V", "credits": 1, "type": "AEC/SDC"},
                {"code": "BNSK658", "name": "NATIONAL SERVICE SCHEME (NSS)", "credits": 0, "type": "MC"},
                {"code": "BPEK658", "name": "PHYSICAL EDUCATION (SPORTS AND ATHLETICS)", "credits": 0, "type": "MC"},
                {"code": "BYOK658", "name": "YOGA", "credits": 0, "type": "MC"},
                {"code": "BIKS609", "name": "INDIAN KNOWLEDGE SYSTEM", "credits": 0, "type": "MC"},
            ],
            "7": [  # 7th Semester (Swappable with 8th)
                {"code": "BCS701", "name": "INTERNET OF THINGS", "credits": 4, "type": "IPCC"},
                {"code": "BCS702", "name": "PARALLEL COMPUTING", "credits": 4, "type": "IPCC"},
                {"code": "BCS703", "name": "CRYPTOGRAPHY & NETWORK SECURITY", "credits": 4, "type": "PCC"},
                {"code": "BCS714x", "name": "PROFESSIONAL ELECTIVE COURSE", "credits": 3, "type": "PEC"},
                {"code": "BCS755x", "name": "OPEN ELECTIVE COURSE", "credits": 3, "type": "OEC"},
                {"code": "BCS786", "name": "MAJOR PROJECT PHASE-II", "credits": 6, "type": "PROJ"},
            ],
            "8": [  # 8th Semester (Swappable with 7th)
                {"code": "BCS801x", "name": "PROFESSIONAL ELECTIVE (ONLINE COURSES) ONLY THROUGH NPTEL", "credits": 3, "type": "PEC"},
                {"code": "BCS802x", "name": "OPEN ELECTIVE (ONLINE COURSES) ONLY THROUGH NPTEL", "credits": 3, "type": "OEC"},
                {"code": "BCS803", "name": "INTERNSHIP (INDUSTRY / RESEARCH) (14 - 20 WEEKS)", "credits": 10, "type": "INT"},
            ],
            # Professional Electives (sample)
            "PEC": [
                {"code": "BCS613A", "name": "BLOCKCHAIN TECHNOLOGY", "credits": 3, "type": "PEC"},
                {"code": "BCS613B", "name": "COMPUTER VISION", "credits": 3, "type": "PEC"},
                {"code": "BCS613C", "name": "COMPILER DESIGN", "credits": 3, "type": "PEC"},
                {"code": "BCS613D", "name": "ADVANCED JAVA", "credits": 3, "type": "PEC"},
            ],
            # Open Electives (sample)
            "OEC": [
                {"code": "BCS654A", "name": "INTRODUCTION TO DATA STRUCTURES", "credits": 3, "type": "OEC"},
                {"code": "BIS654C", "name": "MOBILE APPLICATION DEVELOPMENT", "credits": 3, "type": "OEC"},
                {"code": "BCS654B", "name": "FUNDAMENTALS OF OPERATING SYSTEMS", "credits": 3, "type": "OEC"},
                {"code": "BAI654D", "name": "INTRODUCTION TO ARTIFICIAL INTELLIGENCE", "credits": 3, "type": "OEC"},
            ],
            # Ability Enhancement Course - Skill Enhancement Course (examples)
            "AEC_SEC": [
                {"code": "BISL657A", "name": "TOSCA – AUTOMATED SOFTWARE TESTING", "credits": 1, "type": "AEC/SEC"},
                {"code": "BAIL657C", "name": "GENERATIVE AI", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL657B", "name": "REACT", "credits": 1, "type": "AEC/SEC"},
                {"code": "BCSL657D", "name": "DEVOPS", "credits": 1, "type": "AEC/SEC"},
            ]
        },
        "EC": {  # Electronics & Communication Engineering
            "1": [
                {"code": "BMATS101", "name": "MATHEMATICS-I FOR ECE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BPHYS102", "name": "APPLIED PHYSICS FOR ECE STREAM", "credits": 4, "type": "ASC"},
                {"code": "BEC101", "name": "BASIC ELECTRONICS", "credits": 4, "type": "ESC"},
                {"code": "BEC102", "name": "ELECTRONIC DEVICES", "credits": 4, "type": "ESC"},
                {"code": "BEC103", "name": "DIGITAL ELECTRONICS", "credits": 4, "type": "ESC"},
                {"code": "BEC104", "name": "ANALOG ELECTRONICS", "credits": 4, "type": "ESC"},
                {"code": "BEC105", "name": "SIGNALS AND SYSTEMS", "credits": 4, "type": "ESC"},
                {"code": "BEC106", "name": "COMMUNICATION SYSTEMS", "credits": 4, "type": "ESC"},
                {"code": "BEC107", "name": "MICROWAVE ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC108", "name": "ANTENNA THEORY", "credits": 4, "type": "ESC"},
                {"code": "BEC109", "name": "OPTICAL COMMUNICATION", "credits": 4, "type": "ESC"},
                {"code": "BEC110", "name": "SATELLITE COMMUNICATION", "credits": 4, "type": "ESC"},
                {"code": "BEC111", "name": "MOBILE COMMUNICATION", "credits": 4, "type": "ESC"},
                {"code": "BEC112", "name": "WIRELESS COMMUNICATION", "credits": 4, "type": "ESC"},
                {"code": "BEC113", "name": "NETWORK THEORY", "credits": 4, "type": "ESC"},
                {"code": "BEC114", "name": "CONTROL SYSTEMS", "credits": 4, "type": "ESC"},
                {"code": "BEC115", "name": "DIGITAL SIGNAL PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC116", "name": "IMAGE PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC117", "name": "SPEECH PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC118", "name": "VIDEO PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC119", "name": "AUDIO PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC120", "name": "MULTIMEDIA PROCESSING", "credits": 4, "type": "ESC"},
                {"code": "BEC121", "name": "REAL-TIME SYSTEMS", "credits": 4, "type": "ESC"},
                {"code": "BEC122", "name": "EMBEDDED SYSTEMS", "credits": 4, "type": "ESC"},
                {"code": "BEC123", "name": "VLSI DESIGN", "credits": 4, "type": "ESC"},
                {"code": "BEC124", "name": "CMOS DESIGN", "credits": 4, "type": "ESC"},
                {"code": "BEC125", "name": "ANALOG VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC126", "name": "DIGITAL VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC127", "name": "MIXED SIGNAL VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC128", "name": "RF VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC129", "name": "HIGH SPEED VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC130", "name": "LOW POWER VLSI", "credits": 4, "type": "ESC"},
                {"code": "BEC131", "name": "TESTING AND VERIFICATION", "credits": 4, "type": "ESC"},
                {"code": "BEC132", "name": "DESIGN FOR TESTABILITY", "credits": 4, "type": "ESC"},
                {"code": "BEC133", "name": "BUILT-IN SELF TEST", "credits": 4, "type": "ESC"},
                {"code": "BEC134", "name": "SCAN DESIGN", "credits": 4, "type": "ESC"},
                {"code": "BEC135", "name": "BOUNDARY SCAN", "credits": 4, "type": "ESC"},
                {"code": "BEC136", "name": "MEMORY TESTING", "credits": 4, "type": "ESC"},
                {"code": "BEC137", "name": "LOGIC TESTING", "credits": 4, "type": "ESC"},
                {"code": "BEC138", "name": "FAULT SIMULATION", "credits": 4, "type": "ESC"},
                {"code": "BEC139", "name": "FAULT MODELING", "credits": 4, "type": "ESC"},
                {"code": "BEC140", "name": "FAULT DIAGNOSIS", "credits": 4, "type": "ESC"},
                {"code": "BEC141", "name": "FAULT TOLERANCE", "credits": 4, "type": "ESC"},
                {"code": "BEC142", "name": "RELIABILITY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC143", "name": "MAINTAINABILITY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC144", "name": "AVAILABILITY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC145", "name": "SAFETY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC146", "name": "SECURITY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC147", "name": "PRIVACY ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC148", "name": "TRUST ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC149", "name": "RESILIENCE ENGINEERING", "credits": 4, "type": "ESC"},
                {"code": "BEC150", "name": "ADAPTABILITY ENGINEERING", "credits": 4, "type": "ESC"}
            ]
        }
    },
    
    # ===== 2021 SCHEME =====
    "2021": {
        "CS": {  # Computer Science & Engineering
            "1": [
                {"code": "21MA101", "name": "CALCULUS AND LINEAR ALGEBRA", "credits": 4, "type": "ASC"},
                {"code": "21PH101", "name": "PHYSICS", "credits": 3, "type": "ASC"},
                {"code": "21CH101", "name": "CHEMISTRY", "credits": 3, "type": "ASC"},
                {"code": "21EE101", "name": "BASIC ELECTRICAL ENGINEERING", "credits": 3, "type": "ESC"},
                {"code": "21ME101", "name": "ELEMENTS OF MECHANICAL ENGINEERING", "credits": 3, "type": "ESC"},
                {"code": "21CS101", "name": "PROGRAMMING IN C", "credits": 3, "type": "ESC"},
                {"code": "21EG101", "name": "ENGINEERING GRAPHICS", "credits": 1, "type": "ESC"}
            ],
            "3": [
                {"code": "21MA301", "name": "DISCRETE MATHEMATICS", "credits": 3, "type": "ASC"},
                {"code": "21CS301", "name": "DATA STRUCTURES", "credits": 4, "type": "ESC"},
                {"code": "21CS302", "name": "COMPUTER ORGANIZATION", "credits": 4, "type": "ESC"},
                {"code": "21CS303", "name": "OBJECT ORIENTED PROGRAMMING WITH JAVA", "credits": 4, "type": "ESC"},
                {"code": "21CS304", "name": "DATABASE MANAGEMENT SYSTEMS", "credits": 3, "type": "ESC"},
                {"code": "21CS305", "name": "DATA STRUCTURES LABORATORY", "credits": 2, "type": "ESC"}
            ]
        }
    },
    
    # ===== 2018 SCHEME =====
    "2018": {
        "CS": {  # Computer Science & Engineering
            "1": [
                {"code": "18MA101", "name": "CALCULUS AND LINEAR ALGEBRA", "credits": 4, "type": "ASC"},
                {"code": "18PH101", "name": "PHYSICS", "credits": 3, "type": "ASC"},
                {"code": "18CH101", "name": "CHEMISTRY", "credits": 3, "type": "ASC"},
                {"code": "18EE101", "name": "BASIC ELECTRICAL ENGINEERING", "credits": 3, "type": "ESC"},
                {"code": "18ME101", "name": "ELEMENTS OF MECHANICAL ENGINEERING", "credits": 3, "type": "ESC"},
                {"code": "18CS101", "name": "PROGRAMMING IN C", "credits": 3, "type": "ESC"},
                {"code": "18EG101", "name": "ENGINEERING GRAPHICS", "credits": 1, "type": "ESC"}
            ],
            "3": [
                {"code": "18MA301", "name": "DISCRETE MATHEMATICS", "credits": 3, "type": "ASC"},
                {"code": "18CS301", "name": "DATA STRUCTURES", "credits": 4, "type": "ESC"},
                {"code": "18CS302", "name": "COMPUTER ORGANIZATION", "credits": 4, "type": "ESC"},
                {"code": "18CS303", "name": "OBJECT ORIENTED PROGRAMMING WITH JAVA", "credits": 4, "type": "ESC"},
                {"code": "18CS304", "name": "DATABASE MANAGEMENT SYSTEMS", "credits": 3, "type": "ESC"},
                {"code": "18CS305", "name": "DATA STRUCTURES LABORATORY", "credits": 2, "type": "ESC"}
            ]
        }
    }
}

# FLAT SUBJECTS DICTIONARY FOR EASY LOOKUP
VTU_SUBJECTS_FLAT = {}

def build_flat_subjects():
    """Build a flat dictionary for easy subject lookup by code"""
    for scheme, branches in VTU_SUBJECTS_DATABASE.items():
        for branch, semesters in branches.items():
            for semester, subjects in semesters.items():
                for subject in subjects:
                    VTU_SUBJECTS_FLAT[subject["code"]] = {
                        "name": subject["name"],
                        "credits": subject["credits"],
                        "type": subject["type"],
                        "scheme": scheme,
                        "branch": branch,
                        "semester": semester
                    }

# Build the flat dictionary when module is imported
build_flat_subjects()

def get_subject_info(subject_code):
    """Get subject information by code"""
    return VTU_SUBJECTS_FLAT.get(subject_code.upper(), None)

def get_subjects_by_scheme(scheme):
    """Get all subjects for a specific scheme"""
    return VTU_SUBJECTS_DATABASE.get(scheme, {})

def get_subjects_by_branch(scheme, branch):
    """Get all subjects for a specific scheme and branch"""
    schemes = VTU_SUBJECTS_DATABASE.get(scheme, {})
    return schemes.get(branch, {})

def get_subjects_by_semester(scheme, branch, semester):
    """Get subjects for a specific scheme, branch, and semester"""
    branches = VTU_SUBJECTS_DATABASE.get(scheme, {})
    semesters = branches.get(branch, {})
    return semesters.get(str(semester), [])

def search_subjects(query):
    """Search subjects by name or code"""
    results = []
    query = query.upper()
    
    for code, info in VTU_SUBJECTS_FLAT.items():
        if query in code or query in info["name"].upper():
            results.append({"code": code, **info})
    
    return results

def get_total_credits(scheme, branch):
    """Calculate total credits for a scheme and branch"""
    total = 0
    branches = VTU_SUBJECTS_DATABASE.get(scheme, {})
    semesters = branches.get(branch, {})
    
    for semester, subjects in semesters.items():
        for subject in subjects:
            total += subject["credits"]
    
    return total

# Example usage:
if __name__ == "__main__":
    print("VTU Subjects Database")
    print("=" * 50)
    
    # Get subject info
    subject = get_subject_info("BCS401")
    if subject:
        print(f"BCS401: {subject['name']} ({subject['credits']} credits)")
    
    # Get total credits for CS 2022 scheme
    total = get_total_credits("2022", "CS")
    print(f"Total credits for CS 2022 scheme: {total}")
    
    # Search subjects
    results = search_subjects("algorithm")
    print(f"Found {len(results)} subjects with 'algorithm' in name")
