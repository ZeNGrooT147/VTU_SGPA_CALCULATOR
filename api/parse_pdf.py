from http.server import BaseHTTPRequestHandler
import json
import base64
import requests
import os
from subjects_database import get_subject_info, get_subject_credits, search_subjects
import re

# VTU Grading Schemes
VTU_SCHEMES = {
    "2022": {
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 50: "B", 40: "C", 0: "F"
        },
        "grading": {
            "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0
        }
    },
    "2021": {
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 50: "B", 40: "C", 0: "F"
        },
        "grading": {
            "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0
        }
    },
    "2018": {
        "marks_to_grade": {
            90: "O", 80: "A+", 70: "A", 60: "B+", 50: "B", 40: "C", 0: "F"
        },
        "grading": {
            "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "F": 0
        }
    }
}

def get_subject_credits(subject_code):
    """Get subject credits from the integrated database"""
    # First try the main subjects database
    subject_info = get_subject_info(subject_code)
    if subject_info:
        return subject_info["credits"]
    
    # Default credit for unknown subjects
    return 3

def get_subject_name(subject_code):
    """Get subject name from the integrated database"""
    # First try the main subjects database
    subject_info = get_subject_info(subject_code)
    if subject_info:
        return subject_info["name"]
    
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
    scheme_scores = {}
    
    for scheme, data in VTU_SCHEMES.items():
        score = 0
        
        # Check for scheme-specific keywords
        if scheme == "2022":
            if re.search(r'BCS|BEC|BME|BCV|BEE|BIS|BAD|BBT|BCH', text, re.IGNORECASE):
                score += 50
            # Also check for BCS format (BCS401, BCS402, etc.)
            if re.search(r'BCS\d{3}', text, re.IGNORECASE):
                score += 100
            if re.search(r'2022|22', text, re.IGNORECASE):
                score += 30
        elif scheme == "2021":
            if re.search(r'21CS|21EC|21ME|21CV|21EE|21IS|21AD|21BT|21CH', text, re.IGNORECASE):
                score += 100
            if re.search(r'2021|21', text, re.IGNORECASE):
                score += 30
        elif scheme == "2018":
            if re.search(r'18CS|18EC|18ME|18CV|18EE|18IS|18AD|18BT|18CH', text, re.IGNORECASE):
                score += 100
            if re.search(r'2018|18', text, re.IGNORECASE):
                score += 30
        
        scheme_scores[scheme] = score
    
    # Return the scheme with highest score
    if scheme_scores:
        return max(scheme_scores, key=scheme_scores.get)
    return "2022"  # Default to 2022

def detect_branch_from_text(text):
    """Auto-detect engineering branch from PDF text"""
    branch_keywords = {
        "CS": ["COMPUTER SCIENCE", "CSE", "BCS", "21CS", "18CS", "COMPUTER"],
        "EC": ["ELECTRONICS", "ECE", "BEC", "21EC", "18EC", "COMMUNICATION"],
        "ME": ["MECHANICAL", "BME", "21ME", "18ME", "MECH"],
        "CV": ["CIVIL", "BCV", "21CV", "18CV"],
        "EE": ["ELECTRICAL", "BEE", "21EE", "18EE", "ELECTRICAL"],
        "IS": ["INFORMATION SCIENCE", "BIS", "21IS", "18IS", "ISE"],
        "AD": ["AEROSPACE", "BAD", "21AD", "18AD"],
        "BT": ["BIOTECHNOLOGY", "BBT", "21BT", "18BT"],
        "CH": ["CHEMICAL", "BCH", "21CH", "18CH"]
    }
    
    text_upper = text.upper()
    branch_scores = {}
    
    for branch, keywords in branch_keywords.items():
        score = 0
        for keyword in keywords:
            if keyword in text_upper:
                score += 10
        if score > 0:
            branch_scores[branch] = score
    
    if branch_scores:
        return max(branch_scores, key=branch_scores.get)
    return "CS"  # Default to Computer Science

def parse_pdf_with_ai(pdf_content, api_key):
    """Parse PDF using Gemini AI"""
    try:
        # Encode PDF content
        encoded_content = base64.b64encode(pdf_content).decode('utf-8')
        
        # Gemini API endpoint
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
        
        # Request payload
        payload = {
            "contents": [{
                "parts": [{
                    "text": """Extract the following information from this VTU result PDF:
                    1. Subject codes (e.g., BCS401, BCS402)
                    2. Subject names
                    3. Internal marks
                    4. External marks
                    5. Total marks
                    6. Pass/Fail status
                    
                    Return the data in this exact JSON format:
                    {
                        "subjects": [
                            {
                                "code": "BCS401",
                                "name": "Subject Name",
                                "internal": 45,
                                "external": 36,
                                "total": 81,
                                "result": "P"
                            }
                        ]
                    }
                    
                    Only return the JSON, no other text."""
                }, {
                    "inline_data": {
                        "mime_type": "application/pdf",
                        "data": encoded_content
                    }
                }]
            }]
        }
        
        # Make request to Gemini API
        headers = {"Content-Type": "application/json"}
        params = {"key": api_key}
        
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        content = result.get("candidates", [{}])[0].get("content", {})
        parts = content.get("parts", [{}])
        
        if parts and "text" in parts[0]:
            ai_text = parts[0]["text"]
            
            # Extract JSON from AI response
            json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if json_match:
                ai_data = json.loads(json_match.group())
                return ai_data.get("subjects", [])
        
        return []
        
    except Exception as e:
        print(f"AI parsing error: {str(e)}")
        return []

def parse_pdf_traditional(pdf_content):
    """Traditional PDF parsing using regex patterns"""
    try:
        # Convert PDF content to text (simplified for serverless)
        text = pdf_content.decode('utf-8', errors='ignore')
        
        # Enhanced regex patterns for subject extraction
        patterns = [
            # Pattern 1: BCS401 | ANALYSIS & DESIGN OF ALGORITHMS | 45 | 36 | 81 | P
            r'([A-Z]{3,4}\d{3}[A-Z]?)\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*([PF])',
            # Pattern 2: BCS401 ANALYSIS & DESIGN OF ALGORITHMS 45 36 81 P
            r'([A-Z]{3,4}\d{3}[A-Z]?)\s+([A-Z\s&]+?)\s+(\d+)\s+(\d+)\s+(\d+)\s+([PF])',
            # Pattern 3: Subject Code: BCS401, Internal: 45, External: 36, Total: 81, Result: P
            r'([A-Z]{3,4}\d{3}[A-Z]?).*?(\d+).*?(\d+).*?(\d+).*?([PF])',
        ]
        
        subjects = []
        scheme = detect_scheme_from_text(text)
        branch = detect_branch_from_text(text)
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                for match in matches:
                    if len(match) >= 6:
                        code = match[0].upper()
                        name = match[1].strip()
                        internal = int(match[2])
                        external = int(match[3])
                        total = int(match[4])
                        result = match[5].upper()
                        
                        # Get credits from database
                        credits = get_subject_credits(code)
                        subject_name = get_subject_name(code)
                        
                        # Calculate grade points and grades
                        grade_point = calculate_grade_point(total, scheme)
                        grade_letter = get_grade_from_marks(total, scheme)
                        
                        subjects.append({
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
                        })
                
                if subjects:
                    break
        
        return subjects, scheme, branch
        
    except Exception as e:
        print(f"Traditional parsing error: {str(e)}")
        return [], "2022", "CS"

def calculate_sgpa(subjects):
    """Calculate SGPA from subjects"""
    if not subjects:
        return 0.0
    
    total_credit_points = sum(subject["credit_points"] for subject in subjects)
    total_credits = sum(subject["credits"] for subject in subjects)
    
    if total_credits == 0:
        return 0.0
    
    return round(total_credit_points / total_credits, 2)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Get PDF content and API key
            pdf_content = base64.b64decode(request_data.get('pdf_content', ''))
            api_key = request_data.get('api_key', '')
            
            if not pdf_content:
                self.send_error_response("No PDF content provided")
                return
            
            # Try AI parsing first if API key is provided
            subjects = []
            scheme = "2022"
            branch = "CS"
            
            if api_key:
                subjects = parse_pdf_with_ai(pdf_content, api_key)
                if subjects:
                    # Process AI results
                    for subject in subjects:
                        code = subject.get("code", "")
                        if code:
                            credits = get_subject_credits(code)
                            subject_name = get_subject_name(code)
                            total = subject.get("total", 0)
                            
                            # Calculate grade points and grades
                            grade_point = calculate_grade_point(total, scheme)
                            grade_letter = get_grade_from_marks(total, scheme)
                            
                            subject.update({
                                "grade_point": grade_point,
                                "credits": credits,
                                "grade": grade_letter,
                                "credit_points": grade_point * credits
                            })
            
            # Fallback to traditional parsing if AI fails
            if not subjects:
                subjects, scheme, branch = parse_pdf_traditional(pdf_content)
            
            # Calculate SGPA
            sgpa = calculate_sgpa(subjects)
            
            # Calculate totals
            total_internal = sum(subject.get("internal", 0) for subject in subjects)
            total_external = sum(subject.get("external", 0) for subject in subjects)
            total_overall = sum(subject.get("total", 0) for subject in subjects)
            total_credits = sum(subject.get("credits", 0) for subject in subjects)
            total_credit_points = sum(subject.get("credit_points", 0) for subject in subjects)
            passed_subjects = sum(1 for subject in subjects if subject.get("result", "") == "P")
            
            # Prepare response
            response_data = {
                "success": True,
                "subjects": subjects,
                "scheme": scheme,
                "branch": branch,
                "sgpa": sgpa,
                "summary": {
                    "total_internal": total_internal,
                    "total_external": total_external,
                    "total_overall": total_overall,
                    "total_subjects": len(subjects),
                    "passed_subjects": passed_subjects,
                    "total_credits": total_credits,
                    "total_credit_points": total_credit_points
                }
            }
            
            self.send_success_response(response_data)
            
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            self.send_error_response(f"Error processing PDF: {str(e)}")
    
    def do_GET(self):
        """Handle GET requests for health check"""
        if self.path == "/api/health":
            self.send_success_response({"status": "healthy", "message": "VTU PDF Parser API is running"})
        else:
            self.send_error_response("Method not allowed", 405)
    
    def send_success_response(self, data):
        """Send successful response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, message, status_code=400):
        """Send error response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"success": False, "error": message}).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
