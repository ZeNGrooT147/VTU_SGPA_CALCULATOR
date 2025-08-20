import pdfplumber
import re
import json
import base64
import requests
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import os
from subjects_database import get_subject_info, get_subjects_by_scheme, get_subjects_by_branch, search_subjects

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# VTU Schemes and their grade mappings
VTU_SCHEMES = {
    "2024": {
        "grading": {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0},
        "pattern": r"B[A-Z]{4}\d{3}[A-Z]?",
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 55: "B", 50: "C", 40: "P"
        }
    },
    "2022": {
        "grading": {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0},
        "pattern": r"B[A-Z]{2}\d{3}[A-Z]?",
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 55: "B", 50: "C", 40: "P"
        }
    },
    "2021": {
        "grading": {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0},
        "pattern": r"21[A-Z]{2,4}\d{2,3}",
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 55: "B", 50: "C", 40: "P"
        }
    },
    "2018": {
        "grading": {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 0},
        "pattern": r"18[A-Z]{2,4}\d{2,3}",
        "marks_to_grade": {
            90: "S", 80: "A", 70: "B", 60: "C", 50: "D", 40: "E"
        }
    },
    "2017": {
        "grading": {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 0},
        "pattern": r"17[A-Z]{2,4}\d{2,3}",
        "marks_to_grade": {
            90: "S", 80: "A", 70: "B", 60: "C", 50: "D", 40: "E"
        }
    },
    "2015": {
        "grading": {"S": 10, "A": 9, "B": 8, "C": 7, "D": 6, "E": 5, "F": 0},
        "pattern": r"15[A-Z]{2,4}\d{2,3}",
        "marks_to_grade": {
            90: "S", 80: "A", 70: "B", 60: "C", 50: "D", 40: "E"
        }
    }
}

# VTU Subject Credits Database - Now integrated with subjects_database.py
# This provides a fallback for any subjects not in the main database
SUBJECT_CREDITS = {
    # Fallback credits for subjects not in the main database
    "BCS401": {"name": "ANALYSIS & DESIGN OF ALGORITHMS", "credits": 4},
    "BCS402": {"name": "MICROCONTROLLERS", "credits": 4},
    "BCS403": {"name": "DATABASE MANAGEMENT SYSTEMS", "credits": 4},
    "BCSL404": {"name": "ANALYSIS & DESIGN OF ALGORITHMS LAB", "credits": 1},
    "BBOC407": {"name": "BIOLOGY FOR COMPUTER ENGINEERS", "credits": 2},  # Fixed: was 3, now 2
    "BUHK408": {"name": "UNIVERSAL HUMAN VALUES COURSE", "credits": 1},
    "BYOK459": {"name": "YOGA", "credits": 0},
    "BCS405A": {"name": "DISCRETE MATHEMATICAL STRUCTURES", "credits": 4},
    "BCS456B": {"name": "CAPACITY PLANNING FOR IT", "credits": 1}
}

def get_subject_credits(subject_code):
    """Get subject credits from the integrated database"""
    # First try the main subjects database
    subject_info = get_subject_info(subject_code)
    if subject_info:
        return subject_info["credits"]
    
    # Fallback to the old SUBJECT_CREDITS
    if subject_code in SUBJECT_CREDITS:
        return SUBJECT_CREDITS[subject_code]["credits"]
    
    # Default credit for unknown subjects
    return 3

def get_subject_name(subject_code):
    """Get subject name from the integrated database"""
    # First try the main subjects database
    subject_info = get_subject_info(subject_code)
    if subject_info:
        return subject_info["name"]
    
    # Fallback to the old SUBJECT_CREDITS
    if subject_code in SUBJECT_CREDITS:
        return SUBJECT_CREDITS[subject_code]["name"]
    
    # Return the code if no name found
    return subject_code

def calculate_grade_point(marks, scheme):
    """Calculate grade point based on marks and VTU scheme"""
    if scheme not in VTU_SCHEMES:
        return 0
    
    marks_to_grade = VTU_SCHEMES[scheme]["marks_to_grade"]
    grading = VTU_SCHEMES[scheme]["grading"]
    
    # Find the appropriate grade
    grade = "F"  # Default to F
    for threshold, grade_letter in sorted(marks_to_grade.items(), reverse=True):
        if marks >= threshold:
            grade = grade_letter
            break
    
    # Return grade point
    return grading.get(grade, 0)

def get_grade_from_marks(marks, scheme):
    """Get grade letter directly from marks"""
    if scheme not in VTU_SCHEMES:
        return "F"
    
    marks_to_grade = VTU_SCHEMES[scheme]["marks_to_grade"]
    
    # Find the appropriate grade
    grade = "F"  # Default to F
    for threshold, grade_letter in sorted(marks_to_grade.items(), reverse=True):
        if marks >= threshold:
            grade = grade_letter
            break
    
    return grade

def detect_scheme_from_text(text):
    """Auto-detect VTU scheme from PDF text with enhanced detection"""
    # Enhanced scheme detection with multiple patterns and confidence scoring
    scheme_scores = {}
    
    for scheme, data in VTU_SCHEMES.items():
        score = 0
        pattern = data["pattern"]
        
        # Count matches for this scheme
        matches = re.findall(pattern, text, re.IGNORECASE)
        score += len(matches) * 10  # Each match adds 10 points
        
        # Bonus for multiple matches (indicates this is likely the correct scheme)
        if len(matches) > 1:
            score += 20
        
        # Check for scheme-specific keywords
        if scheme == "2022":
            if re.search(r'BCS|BEC|BME|BCV|BEE|BIS|BAD|BBT|BCH', text, re.IGNORECASE):
                score += 50
            # Also check for BCS format (BCS401, BCS402, etc.)
            if re.search(r'BCS\d{3}', text, re.IGNORECASE):
                score += 100  # High confidence for BCS format
        elif scheme == "2021":
            if re.search(r'21CS|21EC|21ME|21CV|21EE|21IS|21AD|21BT|21CH', text, re.IGNORECASE):
                score += 50
        elif scheme == "2018":
            if re.search(r'18CS|18EC|18ME|18CV|18EE|18IS|18AD|18BT|18CH', text, re.IGNORECASE):
                score += 50
        elif scheme == "2017":
            if re.search(r'17CS|17EC|17ME|17CV|17EE|17IS|17AD|17BT|17CH', text, re.IGNORECASE):
                score += 50
        elif scheme == "2015":
            if re.search(r'15CS|15EC|15ME|15CV|15EE|15IS|15AD|15BT|15CH', text, re.IGNORECASE):
                score += 50
        
        scheme_scores[scheme] = score
    
    # Return the scheme with the highest score
    if scheme_scores:
        best_scheme = max(scheme_scores, key=scheme_scores.get)
        if scheme_scores[best_scheme] > 0:
            return best_scheme
    
    return "2022"  # Default to 2022 scheme (most common)

def parse_vtu_pdf(pdf_file, scheme=None):
    """Parse VTU PDF and extract course information with exceptional robustness"""
    subjects = {}
    
    try:
        # First, try Gemini AI for intelligent parsing
        print("Attempting to parse with Gemini AI...")
        ai_subjects = parse_with_gemini_ai(pdf_file)
        
        if ai_subjects and len(ai_subjects) > 0:
            print(f"Gemini AI successfully extracted {len(ai_subjects)} subjects")
            # Process AI results
            for code, subject_data in ai_subjects.items():
                # Get credits from integrated database
                credits = get_subject_credits(code)
                subject_name = get_subject_name(code)
                
                # Calculate grade points and grades
                grade_point = calculate_grade_point(subject_data["total"], scheme or "2022")
                grade_letter = get_grade_from_marks(subject_data["total"], scheme or "2022")
                
                # Update subject data with correct credits and grades
                ai_subjects[code].update({
                    "grade_point": grade_point,
                    "credits": credits,
                    "grade": grade_letter,
                    "credit_points": grade_point * credits
                })
            
            return ai_subjects, scheme or "2022"
        
        # Fallback to traditional parsing if AI fails
        print("Gemini AI failed, using traditional parsing...")
        
        # Extract text from PDF with multiple strategies
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                # Try multiple text extraction methods
                page_text = page.extract_text()
                if not page_text or len(page_text.strip()) < 10:
                    # Fallback: try to extract text from tables
                    tables = page.extract_tables()
                    for table in tables:
                        for row in table:
                            if row:
                                page_text += " ".join([str(cell) for cell in row if cell]) + "\n"
                
                if page_text:
                    text += page_text + "\n"
        
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = re.sub(r'[^\w\s&()\-\.]', ' ', text)  # Remove special chars but keep important ones
        
        # Auto-detect scheme if not provided
        if not scheme:
            scheme = detect_scheme_from_text(text)
        
        # Ultra-flexible course extraction patterns
        patterns = [
            # Pattern 1: Standard VTU format with result (BCS401 format)
            r"([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)\s+([PFAXWNE])",
            # Pattern 2: Alternative format with result
            r"([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)\s+([A-Z]+)",
            # Pattern 3: Compact format without result
            r"([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z &]+)\s+(\d+)\s+(\d+)\s+(\d+)",
            # Pattern 4: More flexible pattern
            r"([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)",
            # Pattern 5: Very flexible pattern for any course code
            r"([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)",
            # Pattern 6: Legacy VTU format (22CS101 format)
            r"([A-Z]{2}\d{2}[A-Z]{2,4}\d{3})\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)\s+([PFAXWNE])",
            r"([A-Z]{2}\d{2}[A-Z]{2,4}\d{3})\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)",
            # Pattern 7: Ultra-flexible - any course code followed by numbers
            r"([A-Z]{2,5}\d{2,4}[A-Z]?)\s+([A-Z &]+(?: [A-Z]+)*)\s+(\d+)\s+(\d+)\s+(\d+)",
            # Pattern 8: Even more flexible - course code anywhere in line with marks
            r"([A-Z]{2,5}\d{2,4}[A-Z]?)[^0-9]*(\d+)[^0-9]*(\d+)[^0-9]*(\d+)",
        ]
        
        all_matches = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                all_matches.extend(matches)
                break
        
        # If no matches found, try ultra-aggressive parsing
        if not all_matches:
            all_matches = _ultra_aggressive_parsing(text)
        
        # If still no matches, try fallback parsing
        if not all_matches:
            all_matches = _fallback_parsing(text)
        
        # Process all matches
        for match in all_matches:
            if len(match) >= 5:
                code = match[0].strip().upper()
                name = match[1].strip().upper()
                internal = int(match[2]) if str(match[2]).isdigit() else 0
                external = int(match[3]) if str(match[3]).isdigit() else 0
                total = int(match[4]) if str(match[4]).isdigit() else 0
                result = match[5] if len(match) > 5 else "P"
                
                # Get credits from database - try multiple approaches
                subject_info = None
                
                # Get credits from integrated database
                credits = get_subject_credits(code)
                subject_name = get_subject_name(code)
                
                grade_point = calculate_grade_point(total, scheme)
                grade_letter = get_grade_from_marks(total, scheme)
                
                # Check if the subject is actually failed based on marks
                if total < 40:  # VTU passing threshold
                    result = "F"
                elif result in ["F", "FAIL", "ABSENT", "A"]:
                    result = "F"
                else:
                    result = "P"
                
                subjects[code] = {
                    "code": code,
                    "name": subject_name,
                    "internal": internal,
                    "external": external,
                    "total": total,
                    "grade_point": grade_point,
                    "credits": credits,
                    "result": result,
                    "grade": grade_letter,
                    "credit_points": grade_point * credits
                }
        
        return subjects, scheme
        
    except Exception as e:
        print(f"Error parsing PDF: {str(e)}")
        return {}, scheme

def detect_branch_from_subjects(subjects):
    """Auto-detect branch from extracted subjects"""
    if not subjects:
        return "Unknown"
    
    # Count branch-specific course codes
    branch_counts = {
        'CS': 0,  # Computer Science
        'EC': 0,  # Electronics & Communication
        'ME': 0,  # Mechanical Engineering
        'CV': 0,  # Civil Engineering
        'EE': 0,  # Electrical & Electronics
        'IS': 0,  # Information Science
        'AD': 0,  # AI & Data Science
        'BT': 0,  # Biotechnology
        'CH': 0   # Chemical Engineering
    }
    
    for code in subjects.keys():
        code_upper = code.upper()
        
        # 2022 scheme patterns
        if code_upper.startswith('BCS'): branch_counts['CS'] += 1
        elif code_upper.startswith('BEC'): branch_counts['EC'] += 1
        elif code_upper.startswith('BME'): branch_counts['ME'] += 1
        elif code_upper.startswith('BCV'): branch_counts['CV'] += 1
        elif code_upper.startswith('BEE'): branch_counts['EE'] += 1
        elif code_upper.startswith('BIS'): branch_counts['IS'] += 1
        elif code_upper.startswith('BAD'): branch_counts['AD'] += 1
        elif code_upper.startswith('BBT'): branch_counts['BT'] += 1
        elif code_upper.startswith('BCH'): branch_counts['CH'] += 1
        
        # 2021 scheme patterns
        elif code_upper.startswith('21CS'): branch_counts['CS'] += 1
        elif code_upper.startswith('21EC'): branch_counts['EC'] += 1
        elif code_upper.startswith('21ME'): branch_counts['ME'] += 1
        elif code_upper.startswith('21CV'): branch_counts['CV'] += 1
        elif code_upper.startswith('21EE'): branch_counts['EE'] += 1
        elif code_upper.startswith('21IS'): branch_counts['IS'] += 1
        elif code_upper.startswith('21AD'): branch_counts['AD'] += 1
        elif code_upper.startswith('21BT'): branch_counts['BT'] += 1
        elif code_upper.startswith('21CH'): branch_counts['CH'] += 1
        
        # 2018 scheme patterns
        elif code_upper.startswith('18CS'): branch_counts['CS'] += 1
        elif code_upper.startswith('18EC'): branch_counts['EC'] += 1
        elif code_upper.startswith('18ME'): branch_counts['ME'] += 1
        elif code_upper.startswith('18CV'): branch_counts['CV'] += 1
        elif code_upper.startswith('18EE'): branch_counts['EE'] += 1
        elif code_upper.startswith('18IS'): branch_counts['IS'] += 1
        elif code_upper.startswith('18AD'): branch_counts['AD'] += 1
        elif code_upper.startswith('18BT'): branch_counts['BT'] += 1
        elif code_upper.startswith('18CH'): branch_counts['CH'] += 1
        
        # 2017 scheme patterns
        elif code_upper.startswith('17CS'): branch_counts['CS'] += 1
        elif code_upper.startswith('17EC'): branch_counts['EC'] += 1
        elif code_upper.startswith('17ME'): branch_counts['ME'] += 1
        elif code_upper.startswith('17CV'): branch_counts['CV'] += 1
        elif code_upper.startswith('17EE'): branch_counts['EE'] += 1
        elif code_upper.startswith('17IS'): branch_counts['IS'] += 1
        elif code_upper.startswith('17AD'): branch_counts['AD'] += 1
        elif code_upper.startswith('17BT'): branch_counts['BT'] += 1
        elif code_upper.startswith('17CH'): branch_counts['CH'] += 1
        
        # 2015 scheme patterns
        elif code_upper.startswith('15CS'): branch_counts['CS'] += 1
        elif code_upper.startswith('15EC'): branch_counts['EC'] += 1
        elif code_upper.startswith('15ME'): branch_counts['ME'] += 1
        elif code_upper.startswith('15CV'): branch_counts['CV'] += 1
        elif code_upper.startswith('15EE'): branch_counts['EE'] += 1
        elif code_upper.startswith('15IS'): branch_counts['IS'] += 1
        elif code_upper.startswith('15AD'): branch_counts['AD'] += 1
        elif code_upper.startswith('15BT'): branch_counts['BT'] += 1
        elif code_upper.startswith('15CH'): branch_counts['CH'] += 1
    
    # Return the branch with the highest count
    if branch_counts:
        best_branch = max(branch_counts, key=branch_counts.get)
        if branch_counts[best_branch] > 0:
            return best_branch
    
    return "Unknown"

def get_grade_from_points(points, scheme):
    """Get grade letter from grade points"""
    if scheme not in VTU_SCHEMES:
        return "F"
    
    grading = VTU_SCHEMES[scheme]["grading"]
    for grade, point in grading.items():
        if point == points:
            return grade
    return "F"

def calculate_sgpa(subjects):
    """Calculate SGPA using VTU formula with exact precision"""
    total_credits = 0
    total_weighted_points = 0
    failed_subjects = []
    
    for subject in subjects.values():
        # Include all subjects in total credits (even failed ones)
        credits = float(subject["credits"])
        grade_point = float(subject["grade_point"])
        
        total_credits += credits
        total_weighted_points += credits * grade_point
        
        # Track failed subjects
        if subject["result"] == "F" or subject["total"] < 40:
            failed_subjects.append(subject["code"])
    
    sgpa = 0.0
    if total_credits > 0:
        sgpa = round(total_weighted_points / total_credits, 2)
    
    return sgpa, total_credits, total_weighted_points, failed_subjects



@app.route("/", methods=["GET"])
def home():
    """Serve the main HTML page from the user's New folder UI"""
    return send_from_directory('New folder', 'index.html')

@app.route("/style.css", methods=["GET"])
def style_css():
    """Serve CSS from the user's New folder UI"""
    return send_from_directory('New folder', 'style.css')

@app.route("/app.js", methods=["GET"])
def app_js():
    """Serve JS from the user's New folder UI"""
    return send_from_directory('New folder', 'app.js')

@app.route("/parse-pdf", methods=["POST"])
def parse_pdf():
    """Parse PDF and return JSON response"""
    try:
        if "pdf_file" not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "File must be a PDF"}), 400
        
        scheme = request.form.get("scheme", None)
        
        # Parse the PDF
        subjects, detected_scheme = parse_vtu_pdf(pdf_file, scheme)
        
        if not subjects:
            return jsonify({
                "error": "No subjects found in PDF. Please ensure it's a valid VTU result PDF.",
                "detected_scheme": detected_scheme
            }), 400
        
        # Calculate SGPA
        sgpa, total_credits, total_weighted_points, failed_subjects = calculate_sgpa(subjects)
        
        # Auto-detect branch
        detected_branch = detect_branch_from_subjects(subjects)
        
        return jsonify({
            "success": True,
            "scheme": detected_scheme,
            "branch": detected_branch,
            "sgpa": round(sgpa, 2),
            "total_credits": total_credits,
            "total_weighted_points": total_weighted_points,
            "subjects": subjects,
            "subjects_count": len(subjects),
            "failed_subjects": failed_subjects,
            "failed_count": len(failed_subjects),
            "detailed_breakdown": {
                "total_internal": sum(subject["internal"] for subject in subjects.values()),
                "total_external": sum(subject["external"] for subject in subjects.values()),
                "total_marks": sum(subject["total"] for subject in subjects.values()),
                "passed_subjects": len([s for s in subjects.values() if s["result"] == "P"]),
                "failed_subjects_count": len([s for s in subjects.values() if s["result"] == "F"]),
                "average_internal": round(sum(subject["internal"] for subject in subjects.values()) / len(subjects), 2),
                "average_external": round(sum(subject["external"] for subject in subjects.values()) / len(subjects), 2),
                "average_total": round(sum(subject["total"] for subject in subjects.values()) / len(subjects), 2)
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

@app.route("/schemes", methods=["GET"])
def get_schemes():
    """Get supported VTU schemes"""
    return jsonify(VTU_SCHEMES)

@app.route("/subjects", methods=["GET"])
def get_subjects():
    """Get supported subjects"""
    return jsonify(SUBJECT_CREDITS)

@app.route("/debug-pdf", methods=["POST"])
def debug_pdf():
    """Debug endpoint to see what's being extracted from PDF"""
    try:
        if "pdf_file" not in request.files:
            return jsonify({"error": "No PDF file provided"}), 400
        
        pdf_file = request.files["pdf_file"]
        if pdf_file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Extract text from PDF
        with pdfplumber.open(pdf_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        
        # Look for course code patterns
        course_codes = re.findall(r'[A-Z]{1,5}\d{3,4}[A-Z]?', text, re.IGNORECASE)
        
        # Look for lines with numbers (potential marks)
        lines_with_numbers = []
        for line in text.split('\n'):
            numbers = re.findall(r'\b(\d+)\b', line)
            if len(numbers) >= 3:  # At least 3 numbers (internal, external, total)
                lines_with_numbers.append({
                    "line": line.strip(),
                    "numbers": numbers
                })
        
        return jsonify({
            "extracted_text": text[:1000] + "..." if len(text) > 1000 else text,
            "course_codes_found": list(set(course_codes)),
            "lines_with_numbers": lines_with_numbers[:10],  # First 10 lines
            "total_lines": len(text.split('\n')),
            "text_length": len(text)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {str(e)}"}), 500

def _ultra_aggressive_parsing(text):
    """Ultra-aggressive parsing that can handle any VTU format"""
    matches = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if len(line) < 10:  # Skip very short lines
            continue
            
        # Look for ANY course code pattern
        code_patterns = [
            r'([A-Z]{2,5}\d{2,4}[A-Z]?)',  # Standard VTU codes
            r'([A-Z]{2}\d{2}[A-Z]{2,4}\d{3})',  # Legacy format
            r'([A-Z]{3,4}\d{3}[A-Z]?)',  # BCS format
        ]
        
        code = None
        for pattern in code_patterns:
            code_match = re.search(pattern, line, re.IGNORECASE)
            if code_match:
                code = code_match.group(1).upper()
                break
        
        if code:
            # Extract ALL numbers from the line
            numbers = re.findall(r'\b(\d+)\b', line)
            
            # Try to identify which numbers are marks
            if len(numbers) >= 3:
                # Assume first 3 numbers are internal, external, total
                internal = int(numbers[0])
                external = int(numbers[1]) 
                total = int(numbers[2])
                
                # Validate: total should be sum of internal + external (approximately)
                if abs(total - (internal + external)) <= 5:  # Allow small difference
                    # Extract subject name
                    name_part = line[line.find(code) + len(code):].strip()
                    # Remove numbers and special chars from name
                    name = re.sub(r'\d+', '', name_part)
                    name = re.sub(r'[^\w\s&]', ' ', name).strip()
                    name = name[:50] if len(name) > 50 else name  # Limit length
                    
                    if name:
                        matches.append((code, name, internal, external, total, "P"))
    
    return matches

def _fallback_parsing(text):
    """Last resort parsing - extract any course-like data"""
    matches = []
    
    # Split into words and look for patterns
    words = text.split()
    
    for i, word in enumerate(words):
        # Look for course code patterns
        if re.match(r'^[A-Z]{2,5}\d{2,4}[A-Z]?$', word, re.IGNORECASE):
            code = word.upper()
            
            # Look for numbers after this code
            numbers = []
            for j in range(i+1, min(i+10, len(words))):
                if words[j].isdigit() and len(words[j]) <= 3:  # Valid mark
                    numbers.append(int(words[j]))
                    if len(numbers) >= 3:
                        break
            
            if len(numbers) >= 3:
                internal, external, total = numbers[0], numbers[1], numbers[2]
                
                # Try to get subject name from surrounding words
                name_words = []
                for j in range(max(0, i-5), i):
                    if words[j].isalpha() and len(words[j]) > 2:
                        name_words.append(words[j])
                
                name = " ".join(name_words[-3:]) if name_words else "UNKNOWN SUBJECT"
                
                matches.append((code, name.upper(), internal, external, total, "P"))
    
    return matches

def parse_with_gemini_ai(pdf_file):
    """Use Google Gemini AI to intelligently parse VTU PDF results"""
    try:
        # Get Gemini API key from environment
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Warning: GEMINI_API_KEY not found. Using fallback parsing.")
            return None
        
        # Convert PDF to base64
        pdf_content = pdf_file.read()
        pdf_file.seek(0)  # Reset file pointer
        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
        
        # Gemini API endpoint - using the newer gemini-2.0-flash model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        # Prepare the prompt for Gemini
        prompt = """
        You are an expert at reading VTU (Visvesvaraya Technological University) exam result PDFs. 
        
        Extract ONLY the following information from this VTU result PDF:
        1. Subject Code (e.g., BCS401, 22CS101, etc.)
        2. Subject Name
        3. Internal Marks
        4. External Marks  
        5. Total Marks
        6. Result (P/F/A/W/X/NE)
        
        Ignore all other information like student details, dates, headers, footers, etc.
        
        Return the data as a clean JSON array of objects with this exact format:
        [
            {
                "code": "BCS401",
                "name": "ANALYSIS & DESIGN OF ALGORITHMS",
                "internal": 49,
                "external": 36,
                "total": 85,
                "result": "P"
            }
        ]
        
        If you cannot find any subjects, return an empty array [].
        Be very precise and accurate with the numbers and codes.
        Only return the JSON array, no additional text or explanations.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "application/pdf",
                            "data": pdf_base64
                        }
                    }
                ]
            }]
        }
        
        # Make API request
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract the response text
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    response_text = content['parts'][0]['text']
                    
                    # Try to extract JSON from the response
                    try:
                        # Look for JSON array in the response
                        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                        if json_match:
                            subjects_data = json.loads(json_match.group())
                            
                            # Convert to our internal format
                            subjects = {}
                            for subject in subjects_data:
                                code = subject.get('code', '').upper()
                                if code:
                                    subjects[code] = {
                                        "code": code,
                                        "name": subject.get('name', 'UNKNOWN SUBJECT'),
                                        "internal": int(subject.get('internal', 0)),
                                        "external": int(subject.get('external', 0)),
                                        "total": int(subject.get('total', 0)),
                                        "grade_point": 0,  # Will be calculated later
                                        "credits": 0,  # Will be assigned later
                                        "result": subject.get('result', 'P'),
                                        "grade": 'F',  # Will be calculated later
                                        "credit_points": 0  # Will be calculated later
                                    }
                            
                            print(f"Gemini AI successfully extracted {len(subjects)} subjects")
                            return subjects
                    
                    except json.JSONDecodeError as e:
                        print(f"Error parsing Gemini response as JSON: {e}")
                        print(f"Response text: {response_text[:500]}...")
        
        print(f"Gemini API request failed: {response.status_code}")
        return None
        
    except Exception as e:
        print(f"Error using Gemini AI: {str(e)}")
        return None

if __name__ == "__main__":
    # Check for Gemini API key
    if not os.getenv('GEMINI_API_KEY'):
        print("\n" + "="*60)
        print("GEMINI AI INTEGRATION SETUP")
        print("="*60)
        print("To use Gemini AI for intelligent PDF parsing:")
        print("1. Get a free API key from: https://makersuite.google.com/app/apikey")
        print("2. Set environment variable: set GEMINI_API_KEY=your_api_key_here")
        print("3. Restart the server")
        print("="*60)
        print("The app will work without Gemini API key using traditional parsing.\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
