// VTU SGPA Calculator - 2022 Scheme
class VTUSGPACalculator {
    constructor() {
        // VTU 2022 Grading System
        this.vtuGrading = {
            "O": { points: 10, range: "90-100", level: "Outstanding" },
            "A+": { points: 9, range: "80-89", level: "Excellent" },
            "A": { points: 8, range: "70-79", level: "Very Good" },
            "B+": { points: 7, range: "60-69", level: "Good" },
            "B": { points: 6, range: "55-59", level: "Above Average" },
            "C": { points: 5, range: "50-54", level: "Average" },
            "P": { points: 4, range: "40-49", level: "Pass" },
            "F": { points: 0, range: "0-39", level: "Fail" }
        };

        // Special grades
        this.specialGrades = {
            "DX": { points: 0, description: "Attendance below 75%" },
            "AU": { points: 0, description: "Audit course" },
            "AB": { points: 0, description: "Absent" },
            "IC": { points: 0, description: "Incomplete" },
            "W": { points: 0, description: "Withdrawn" }
        };

        // VTU Branches
        this.branches = {
            "CS": "Computer Science & Engineering",
            "EC": "Electronics & Communication Engineering", 
            "ME": "Mechanical Engineering",
            "CE": "Civil Engineering",
            "IS": "Information Science & Engineering",
            "EE": "Electrical Engineering",
            "CH": "Chemical Engineering",
            "BT": "Biotechnology",
            "AE": "Aerospace Engineering",
            "IE": "Industrial Engineering"
        };

        // Sample courses for different semesters
        this.sampleCourses = {
            "1": [
                { code: "22MA101", name: "Calculus and Linear Algebra", credits: 4 },
                { code: "22PH101", name: "Physics", credits: 3 },
                { code: "22CH101", name: "Chemistry", credits: 3 },
                { code: "22EE101", name: "Basic Electrical Engineering", credits: 3 },
                { code: "22ME101", name: "Elements of Mechanical Engineering", credits: 3 },
                { code: "22CS101", name: "Programming in C", credits: 3 },
                { code: "22EG101", name: "Engineering Graphics", credits: 1 }
            ],
            "3": [
                { code: "22MA301", name: "Discrete Mathematics", credits: 3 },
                { code: "22CS301", name: "Data Structures", credits: 4 },
                { code: "22CS302", name: "Computer Organization", credits: 4 },
                { code: "22CS303", name: "Object Oriented Programming with Java", credits: 4 },
                { code: "22CS304", name: "Database Management Systems", credits: 3 },
                { code: "22CS305", name: "Data Structures Laboratory", credits: 2 }
            ]
        };

        this.courses = [];
        this.maxCreditsPerSemester = 28;
        this.currentTab = 'pdf-upload';

        this.initializeApp();
    }

    initializeApp() {
        // Initialize PDF.js
        if (typeof pdfjsLib !== 'undefined') {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        }

        this.initializeEventListeners();
        this.populateGradeOptions();
        this.updateCurrentDate();
    }

    initializeEventListeners() {
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabId = e.target.getAttribute('data-tab');
                this.switchToTab(tabId);
            });
        });

        // PDF upload
        const pdfInput = document.getElementById('pdfInput');
        const uploadArea = document.getElementById('uploadArea');

        if (pdfInput) {
            pdfInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        // Drag and drop for PDF
        if (uploadArea) {
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0 && files[0].type === 'application/pdf') {
                    this.processPDF(files[0]);
                }
            });
        }

        // Manual entry form
        this.addEventListenerSafe('addCourseBtn', 'click', () => this.addCourse());
        this.addEventListenerSafe('calculateSGPABtn', 'click', () => this.calculateSGPA());

        // Mark input for automatic grade conversion
        this.addEventListenerSafe('marksInput', 'input', (e) => this.convertMarksToGrade(e.target.value));

        // PDF parsing
        this.addEventListenerSafe('parseDataBtn', 'click', () => this.parseExtractedText());

        // Results actions
        this.addEventListenerSafe('exportPDFBtn', 'click', () => this.exportResults());
        this.addEventListenerSafe('printGradeSheet', 'click', () => this.printGradeSheet());
        this.addEventListenerSafe('shareResults', 'click', () => this.shareResults());
        this.addEventListenerSafe('resetCalculator', 'click', () => this.resetCalculator());

        // Semester selection for sample courses
        this.addEventListenerSafe('semesterSelect', 'change', (e) => this.loadSampleCourses(e.target.value));
    }

    addEventListenerSafe(elementId, event, callback) {
        const element = document.getElementById(elementId);
        if (element) {
            element.addEventListener(event, callback);
        }
    }

    switchToTab(tabId) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');

        this.currentTab = tabId;
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file && file.type === 'application/pdf') {
            this.processPDF(file);
        } else {
            this.showStatus('Please select a valid PDF file.', 'error');
        }
    }

    async processPDF(file) {
        // New flow: send PDF to backend for precise auto-detection (scheme, branch, subjects)
        this.showLoading('Processing VTU Transcript...', 'Using AI to intelligently parse your VTU results...');
        this.showSection('processingSection');
        this.updateProgress(25);

        try {
            const formData = new FormData();
            formData.append('pdf_file', file);

            this.updateProgress(60);
            this.showLoading('AI Processing...', 'Gemini AI is analyzing your VTU transcript...');

            const response = await fetch('/parse-pdf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            if (result.error) {
                throw new Error(result.error);
            }

            this.updateProgress(100);
            this.hideLoading();
            this.renderBackendResults(result);

        } catch (error) {
            console.error('Error processing PDF:', error);
            this.showStatus(`Error processing PDF: ${error.message}`, 'error');
            this.hideLoading();
        }
    }

    renderBackendResults(result) {
        // Build breakdown from backend subjects
        const subjects = Object.values(result.subjects || {});
        const breakdown = subjects.map(s => {
            const credits = Number(s.credits || 0);
            const gradePoints = Number(s.grade_point || 0);
            const creditPoints = credits * gradePoints;
            return {
                code: s.code,
                name: s.name,
                credits: credits,
                grade: s.grade,
                gradePoints: gradePoints,
                creditPoints: creditPoints,
                internal: Number(s.internal || 0),
                external: Number(s.external || 0),
                total: Number(s.total || 0),
                result: s.result || 'P'
            };
        });

        const totalCredits = Number(result.total_credits || breakdown.reduce((sum, c) => sum + c.credits, 0));
        const totalCreditPoints = Number(
            (result.total_weighted_points !== undefined ? result.total_weighted_points : breakdown.reduce((sum, c) => sum + c.creditPoints, 0))
        );
        const sgpa = Number(result.sgpa || (totalCredits > 0 ? totalCreditPoints / totalCredits : 0));
        const percentage = Math.max(0, (sgpa - 0.75) * 10);

        // Update UI using existing helpers
        this.updateResults(sgpa, percentage, totalCredits, totalCreditPoints, breakdown);

        // Update detailed statistics
        this.updateDetailedStatistics(result, breakdown);

        // Override header info with auto-detected details
        const branchMap = {
            'CS': 'Computer Science & Engineering',
            'EC': 'Electronics & Communication',
            'ME': 'Mechanical Engineering',
            'CV': 'Civil Engineering',
            'EE': 'Electrical & Electronics',
            'IS': 'Information Science',
            'AD': 'AI & Data Science',
            'BT': 'Biotechnology',
            'CH': 'Chemical Engineering'
        };
        const sheetBranchEl = document.getElementById('sheetBranch');
        if (sheetBranchEl) sheetBranchEl.textContent = branchMap[result.branch] || result.branch || '-';
        const sheetSemesterEl = document.getElementById('sheetSemester');
        if (sheetSemesterEl) sheetSemesterEl.textContent = 'Auto-detected';

        // Jump straight to results
        this.switchToTab('results');
        // Ensure processing section hidden
        this.hideSection('processingSection');
        this.showStatus('Parsed successfully from PDF. Showing results.', 'success');
    }

    updateDetailedStatistics(result, breakdown) {
        // Create or update detailed breakdown section
        let detailedBreakdownSection = document.getElementById('detailedBreakdownSection');
        if (!detailedBreakdownSection) {
            detailedBreakdownSection = document.createElement('div');
            detailedBreakdownSection.id = 'detailedBreakdownSection';
            detailedBreakdownSection.className = 'card breakdown-card';
            
            // Insert after the main stats grid
            const mainStatsGrid = document.querySelector('.stats-grid');
            if (mainStatsGrid) {
                mainStatsGrid.parentNode.insertBefore(detailedBreakdownSection, mainStatsGrid.nextSibling);
            }
        }

        // Create detailed breakdown table
        detailedBreakdownSection.innerHTML = `
            <div class="card__body">
                <h3>Complete Subject Breakdown</h3>
                <p class="text-secondary">Detailed marks and results for each subject</p>
                
                <div class="table-container">
                    <table class="vtu-table detailed-breakdown-table">
                        <thead>
                            <tr>
                                <th>Subject Code</th>
                                <th>Subject Name</th>
                                <th>Internal</th>
                                <th>External</th>
                                <th>Total</th>
                                <th>Result</th>
                                <th>Credits</th>
                                <th>Grade</th>
                                <th>Grade Points</th>
                                <th>Credit Points</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${breakdown.map(subject => `
                                <tr class="${subject.result === 'F' ? 'fail-row' : 'pass-row'}">
                                    <td><strong>${subject.code}</strong></td>
                                    <td>${subject.name}</td>
                                    <td class="marks-cell internal">${subject.internal}</td>
                                    <td class="marks-cell external">${subject.external}</td>
                                    <td class="marks-cell total">${subject.total}</td>
                                    <td><span class="result-badge ${subject.result === 'P' ? 'pass' : 'fail'}">${subject.result}</span></td>
                                    <td class="credits-cell">${subject.credits}</td>
                                    <td class="grade-cell">${subject.grade}</td>
                                    <td class="grade-points-cell">${subject.gradePoints}</td>
                                    <td class="credit-points-cell"><strong>${subject.creditPoints.toFixed(1)}</strong></td>
                                </tr>
                            `).join('')}
                        </tbody>
                        <tfoot>
                            <tr class="total-row">
                                <td colspan="2"><strong>TOTAL</strong></td>
                                <td><strong>${breakdown.reduce((sum, s) => sum + s.internal, 0)}</strong></td>
                                <td><strong>${breakdown.reduce((sum, s) => sum + s.external, 0)}</strong></td>
                                <td><strong>${breakdown.reduce((sum, s) => sum + s.total, 0)}</strong></td>
                                <td><strong>${breakdown.filter(s => s.result === 'P').length}/${breakdown.length}</strong></td>
                                <td><strong>${breakdown.reduce((sum, s) => sum + s.credits, 0)}</strong></td>
                                <td>-</td>
                                <td>-</td>
                                <td><strong>${breakdown.reduce((sum, s) => sum + s.creditPoints, 0).toFixed(1)}</strong></td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
                
                <div class="breakdown-summary">
                    <div class="summary-grid">
                        <div class="summary-item">
                            <span class="summary-label">Total Internal Marks:</span>
                            <span class="summary-value">${breakdown.reduce((sum, s) => sum + s.internal, 0)}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Total External Marks:</span>
                            <span class="summary-value">${breakdown.reduce((sum, s) => sum + s.external, 0)}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Total Marks:</span>
                            <span class="summary-value">${breakdown.reduce((sum, s) => sum + s.total, 0)}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Passed Subjects:</span>
                            <span class="summary-value success">${breakdown.filter(s => s.result === 'P').length}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Failed Subjects:</span>
                            <span class="summary-value error">${breakdown.filter(s => s.result === 'F').length}</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Total Credits:</span>
                            <span class="summary-value">${breakdown.reduce((sum, s) => sum + s.credits, 0)}</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    parseExtractedText() {
        const text = document.getElementById('extractedText').value;
        if (!text.trim()) {
            this.showStatus('No text found to parse.', 'error');
            return;
        }

        this.showLoading('Parsing VTU Course Data...', 'Identifying courses, grades, and credits');
        
        this.courses = [];
        const lines = text.split('\n').filter(line => line.trim());
        
        // VTU specific parsing patterns
        const vtuCoursePattern = /\b\d{2}[A-Z]{2,4}\d{3}\b/g;
        const gradePattern = /\b(O|A\+|A|B\+|B|C|P|F|DX|AU|AB|IC|W)\b/g;
        const creditPattern = /\b[1-4]\b/g;

        for (let line of lines) {
            const courseData = this.parseVTULine(line);
            if (courseData) {
                this.courses.push(courseData);
            }
        }

        // If no courses found, provide sample data
        if (this.courses.length === 0) {
            const semester = document.getElementById('semesterSelect').value || '3';
            this.loadSampleCourses(semester);
            this.showStatus('Auto-parsing found limited data. Sample courses loaded. Please review and edit.', 'warning');
        } else {
            this.showStatus(`Successfully parsed ${this.courses.length} courses from VTU transcript.`, 'success');
        }

        this.hideLoading();
        this.populateManualTable();
        this.switchToTab('manual-entry');
    }

    parseVTULine(line) {
        // VTU course code pattern: YYCCNNN (e.g., 22CS101)
        const courseCodeMatch = line.match(/\b\d{2}[A-Z]{2,4}\d{3}\b/);
        if (!courseCodeMatch) return null;

        const courseCode = courseCodeMatch[0];
        
        // Look for VTU grades
        const gradeMatch = line.match(/\b(O|A\+|A|B\+|B|C|P|F)\b/);
        const grade = gradeMatch ? gradeMatch[0] : 'A';

        // Look for credits (typically 1-4 for VTU)
        const creditMatch = line.match(/\b[1-4]\b/g);
        let credits = 3; // Default
        if (creditMatch) {
            credits = parseInt(creditMatch[0]);
        }

        // Extract course name
        let courseName = '';
        const codeIndex = line.indexOf(courseCode);
        const gradeIndex = gradeMatch ? line.lastIndexOf(grade) : -1;
        
        if (codeIndex !== -1) {
            const startIndex = codeIndex + courseCode.length;
            const endIndex = gradeIndex !== -1 ? gradeIndex : line.length;
            courseName = line.substring(startIndex, endIndex)
                .replace(/\b\d+\b/g, '') // Remove numbers
                .replace(/[|]/g, ' ') // Replace pipes with spaces
                .trim() || 'Course Name';
        }

        return {
            code: courseCode,
            name: courseName,
            credits: credits,
            grade: grade
        };
    }

    loadSampleCourses(semester) {
        if (semester && this.sampleCourses[semester]) {
            this.courses = this.sampleCourses[semester].map(course => ({
                ...course,
                grade: 'A+' // Default grade
            }));
            this.populateManualTable();
        }
    }

    addCourse() {
        const courseCode = document.getElementById('courseCode').value.trim();
        const courseName = document.getElementById('courseName').value.trim();
        const courseCredits = parseInt(document.getElementById('courseCredits').value);
        const selectedGrade = document.getElementById('gradeSelect').value;
        const marksInput = document.getElementById('marksInput').value;

        // Validation
        if (!courseCode) {
            this.showStatus('Please enter a course code.', 'error');
            return;
        }

        if (!courseName) {
            this.showStatus('Please enter a course name.', 'error');
            return;
        }

        // Validate VTU course code format
        if (!this.validateVTUCourseCode(courseCode)) {
            this.showStatus('Please enter a valid VTU course code (format: YYCCNNN, e.g., 22CS101).', 'error');
            return;
        }

        // Check for duplicate course codes
        if (this.courses.some(course => course.code === courseCode)) {
            this.showStatus('Course code already exists. Please use a different code.', 'error');
            return;
        }

        // Determine grade (from marks or direct selection)
        let finalGrade = selectedGrade;
        if (marksInput) {
            finalGrade = this.marksToGrade(parseInt(marksInput));
        }

        // Check credit limits
        const totalCredits = this.courses.reduce((sum, course) => sum + course.credits, 0) + courseCredits;
        if (totalCredits > this.maxCreditsPerSemester) {
            this.showStatus(`Adding this course would exceed the maximum of ${this.maxCreditsPerSemester} credits per semester.`, 'warning');
        }

        const newCourse = {
            code: courseCode,
            name: courseName,
            credits: courseCredits,
            grade: finalGrade
        };

        this.courses.push(newCourse);
        this.populateManualTable();
        this.clearCourseForm();
        this.calculateSGPA();
        
        this.showStatus(`Course ${courseCode} added successfully.`, 'success');
    }

    validateVTUCourseCode(code) {
        // VTU format: YYCCNNN (e.g., 22CS101, 22MA201)
        const vtuPattern = /^\d{2}[A-Z]{2,4}\d{3}$/;
        return vtuPattern.test(code);
    }

    marksToGrade(marks) {
        if (marks >= 90) return 'O';
        if (marks >= 80) return 'A+';
        if (marks >= 70) return 'A';
        if (marks >= 60) return 'B+';
        if (marks >= 55) return 'B';
        if (marks >= 50) return 'C';
        if (marks >= 40) return 'P';
        return 'F';
    }

    convertMarksToGrade(marks) {
        const marksNum = parseInt(marks);
        if (marksNum >= 0 && marksNum <= 100) {
            const grade = this.marksToGrade(marksNum);
            document.getElementById('gradeSelect').value = grade;
        }
    }

    clearCourseForm() {
        document.getElementById('courseCode').value = '';
        document.getElementById('courseName').value = '';
        document.getElementById('courseCredits').value = '3';
        document.getElementById('gradeSelect').value = 'A+';
        document.getElementById('marksInput').value = '';
    }

    populateManualTable() {
        const tbody = document.getElementById('courseTableBody');
        if (!tbody) return;

        tbody.innerHTML = '';

        this.courses.forEach((course, index) => {
            const row = this.createCourseRow(course, index);
            tbody.appendChild(row);
        });

        this.updateCreditSummary();
        this.showSection('courseTableSection');
    }

    createCourseRow(course, index) {
        const row = document.createElement('tr');
        
        // Course Code
        const codeCell = document.createElement('td');
        const codeInput = document.createElement('input');
        codeInput.type = 'text';
        codeInput.value = course.code;
        codeInput.addEventListener('change', (e) => {
            this.courses[index].code = e.target.value;
            this.calculateSGPA();
        });
        codeCell.appendChild(codeInput);

        // Course Name  
        const nameCell = document.createElement('td');
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.value = course.name;
        nameInput.addEventListener('change', (e) => {
            this.courses[index].name = e.target.value;
        });
        nameCell.appendChild(nameInput);

        // Credits
        const creditsCell = document.createElement('td');
        const creditsSelect = document.createElement('select');
        [1, 2, 3, 4].forEach(credit => {
            const option = document.createElement('option');
            option.value = credit;
            option.textContent = credit;
            if (credit === course.credits) option.selected = true;
            creditsSelect.appendChild(option);
        });
        creditsSelect.addEventListener('change', (e) => {
            this.courses[index].credits = parseInt(e.target.value);
            this.updateCreditSummary();
            this.calculateSGPA();
        });
        creditsCell.appendChild(creditsSelect);

        // Grade
        const gradeCell = document.createElement('td');
        const gradeSelect = this.createGradeSelect(course.grade);
        gradeSelect.addEventListener('change', (e) => {
            this.courses[index].grade = e.target.value;
            this.calculateSGPA();
        });
        gradeCell.appendChild(gradeSelect);

        // Grade Points (calculated)
        const gradePointsCell = document.createElement('td');
        const gradePoints = this.vtuGrading[course.grade]?.points || 0;
        gradePointsCell.textContent = gradePoints;
        gradePointsCell.className = 'font-bold';

        // Credit Points (calculated)
        const creditPointsCell = document.createElement('td');
        const creditPoints = course.credits * gradePoints;
        creditPointsCell.textContent = creditPoints.toFixed(1);
        creditPointsCell.className = 'font-bold';

        // Actions
        const actionsCell = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'btn-delete';
        deleteBtn.innerHTML = '🗑️';
        deleteBtn.title = 'Delete Course';
        deleteBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to delete this course?')) {
                this.courses.splice(index, 1);
                this.populateManualTable();
                this.calculateSGPA();
            }
        });
        actionsCell.appendChild(deleteBtn);

        row.appendChild(codeCell);
        row.appendChild(nameCell);
        row.appendChild(creditsCell);
        row.appendChild(gradeCell);
        row.appendChild(gradePointsCell);
        row.appendChild(creditPointsCell);
        row.appendChild(actionsCell);

        return row;
    }

    createGradeSelect(selectedGrade) {
        const select = document.createElement('select');
        
        Object.keys(this.vtuGrading).forEach(grade => {
            const option = document.createElement('option');
            option.value = grade;
            option.textContent = `${grade} (${this.vtuGrading[grade].points})`;
            if (grade === selectedGrade) {
                option.selected = true;
            }
            select.appendChild(option);
        });

        return select;
    }

    updateCreditSummary() {
        const totalCredits = this.courses.reduce((sum, course) => sum + course.credits, 0);
        const currentCreditsEl = document.getElementById('currentCredits');
        const creditLimitEl = document.getElementById('creditLimit');
        
        if (currentCreditsEl) {
            currentCreditsEl.textContent = totalCredits;
        }

        if (creditLimitEl) {
            creditLimitEl.className = 'credit-limit';
            if (totalCredits > this.maxCreditsPerSemester) {
                creditLimitEl.classList.add('error');
                creditLimitEl.textContent = `Exceeds maximum: ${this.maxCreditsPerSemester} credits per semester`;
            } else if (totalCredits > this.maxCreditsPerSemester * 0.8) {
                creditLimitEl.classList.add('warning');
                creditLimitEl.textContent = `Approaching limit: ${this.maxCreditsPerSemester} credits per semester`;
            } else {
                creditLimitEl.textContent = `Maximum: ${this.maxCreditsPerSemester} credits per semester`;
            }
        }
    }

    calculateSGPA() {
        if (this.courses.length === 0) {
            this.showStatus('Please add at least one course to calculate SGPA.', 'warning');
            return;
        }

        let totalCredits = 0;
        let totalCreditPoints = 0;

        const breakdown = this.courses.map(course => {
            const gradePoints = this.vtuGrading[course.grade]?.points || 0;
            const creditPoints = course.credits * gradePoints;
            
            totalCredits += course.credits;
            totalCreditPoints += creditPoints;

            return {
                code: course.code,
                name: course.name,
                credits: course.credits,
                grade: course.grade,
                gradePoints: gradePoints,
                creditPoints: creditPoints
            };
        });

        // VTU SGPA Formula: ∑(Ci × Gi) / ∑Ci
        const sgpa = totalCredits > 0 ? totalCreditPoints / totalCredits : 0;
        
        // VTU percentage conversion: (SGPA - 0.75) × 10
        const percentage = Math.max(0, (sgpa - 0.75) * 10);

        this.updateResults(sgpa, percentage, totalCredits, totalCreditPoints, breakdown);
        this.populateGradeSheet(breakdown, sgpa, totalCredits, totalCreditPoints);
        this.switchToTab('results');
    }

    updateResults(sgpa, percentage, totalCredits, totalCreditPoints, breakdown) {
        // Update main SGPA display
        const sgpaValueEl = document.getElementById('sgpaValue');
        if (sgpaValueEl) {
            sgpaValueEl.textContent = sgpa.toFixed(2);
        }

        // Update percentage
        const percentageValueEl = document.getElementById('percentageValue');
        if (percentageValueEl) {
            percentageValueEl.textContent = percentage.toFixed(1) + '%';
        }

        // Update performance badge
        this.updatePerformanceBadge(sgpa);

        // Update statistics
        this.updateStatistics(totalCredits, totalCreditPoints, breakdown);

        // Update breakdown
        this.updateBreakdown(breakdown, totalCredits, totalCreditPoints, sgpa);
    }

    updatePerformanceBadge(sgpa) {
        const badge = document.getElementById('performanceBadge');
        if (!badge) return;

        let className = 'performance-badge';
        let text = '';

        if (sgpa >= 9.0) {
            className += ' outstanding';
            text = 'Outstanding';
        } else if (sgpa >= 8.0) {
            className += ' excellent'; 
            text = 'Excellent';
        } else if (sgpa >= 7.0) {
            className += ' good';
            text = 'Good';
        } else if (sgpa >= 6.0) {
            className += ' average';
            text = 'Above Average';
        } else if (sgpa >= 5.0) {
            className += ' average';
            text = 'Average';
        } else {
            className += ' average';
            text = 'Needs Improvement';
        }

        badge.className = className;
        badge.textContent = text;
    }

    updateStatistics(totalCredits, totalCreditPoints, breakdown) {
        // Total credits
        const totalCreditsEl = document.getElementById('totalCreditsResult');
        if (totalCreditsEl) {
            totalCreditsEl.textContent = totalCredits;
        }

        // Total credit points
        const totalCreditPointsEl = document.getElementById('totalCreditPointsResult');
        if (totalCreditPointsEl) {
            totalCreditPointsEl.textContent = totalCreditPoints.toFixed(1);
        }

        // Average grade
        const avgGradeEl = document.getElementById('averageGradeResult');
        if (avgGradeEl && breakdown.length > 0) {
            const avgGradePoints = totalCreditPoints / totalCredits;
            const avgGrade = this.gradePointsToGrade(avgGradePoints);
            avgGradeEl.textContent = avgGrade;
        }
    }

    gradePointsToGrade(points) {
        if (points >= 9.5) return 'O';
        if (points >= 8.5) return 'A+';
        if (points >= 7.5) return 'A';
        if (points >= 6.5) return 'B+';
        if (points >= 5.5) return 'B';
        if (points >= 4.5) return 'C';
        if (points >= 3.5) return 'P';
        return 'F';
    }

    updateBreakdown(breakdown, totalCredits, totalCreditPoints, sgpa) {
        const container = document.getElementById('calculationBreakdown');
        if (!container) return;

        container.innerHTML = '';

        // Course breakdown
        breakdown.forEach(course => {
            const item = document.createElement('div');
            item.className = 'breakdown-item';
            item.innerHTML = `
                <span>${course.code}: ${course.credits} × ${course.gradePoints}</span>
                <span>${course.creditPoints.toFixed(1)} points</span>
            `;
            container.appendChild(item);
        });

        // Total calculation
        const totalItem = document.createElement('div');
        totalItem.className = 'breakdown-item breakdown-total';
        totalItem.innerHTML = `
            <span>SGPA = ${totalCreditPoints.toFixed(1)} ÷ ${totalCredits}</span>
            <span>${sgpa.toFixed(2)}</span>
        `;
        container.appendChild(totalItem);
    }

    populateGradeSheet(breakdown, sgpa, totalCredits, totalCreditPoints) {
        // Update sheet info
        const semesterEl = document.getElementById('sheetSemester');
        const branchEl = document.getElementById('sheetBranch');
        
        if (semesterEl) {
            const semester = document.getElementById('semesterSelect').value;
            semesterEl.textContent = semester === 'lateral' ? 'Lateral Entry' : 
                                    semester ? `${semester}${this.getOrdinalSuffix(semester)} Semester` : 'Not Selected';
        }

        if (branchEl) {
            const branch = document.getElementById('branchSelect').value;
            branchEl.textContent = branch ? this.branches[branch] : 'Not Selected';
        }

        // Populate grade sheet table with detailed information
        const tbody = document.getElementById('gradeSheetBody');
        if (tbody) {
            tbody.innerHTML = '';

            breakdown.forEach(course => {
                const row = document.createElement('tr');
                const resultClass = course.result === 'F' ? 'fail-row' : 'pass-row';
                row.className = resultClass;
                
                row.innerHTML = `
                    <td>${course.code}</td>
                    <td>${course.name}</td>
                    <td>${course.internal}</td>
                    <td>${course.external}</td>
                    <td>${course.total}</td>
                    <td><span class="result-badge ${course.result === 'P' ? 'pass' : 'fail'}">${course.result}</span></td>
                    <td>${course.credits}</td>
                    <td>${course.grade}</td>
                    <td>${course.gradePoints}</td>
                    <td>${course.creditPoints.toFixed(1)}</td>
                `;
                tbody.appendChild(row);
            });
        }

        // Update totals
        const elements = {
            'sheetTotalCredits': totalCredits,
            'sheetTotalCreditPoints': totalCreditPoints.toFixed(1),
            'sheetSGPA': sgpa.toFixed(2)
        };

        Object.entries(elements).forEach(([id, value]) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        });
    }

    getOrdinalSuffix(num) {
        const j = num % 10;
        const k = num % 100;
        if (j == 1 && k != 11) return 'st';
        if (j == 2 && k != 12) return 'nd';
        if (j == 3 && k != 13) return 'rd';
        return 'th';
    }

    populateGradeOptions() {
        const gradeSelect = document.getElementById('gradeSelect');
        if (gradeSelect) {
            gradeSelect.innerHTML = '';
            Object.entries(this.vtuGrading).forEach(([grade, info]) => {
                const option = document.createElement('option');
                option.value = grade;
                option.textContent = `${grade} - ${info.level} (${info.points})`;
                gradeSelect.appendChild(option);
            });
        }
    }

    updateCurrentDate() {
        const dateEl = document.getElementById('sheetDate');
        if (dateEl) {
            dateEl.textContent = new Date().toLocaleDateString('en-IN', {
                year: 'numeric',
                month: 'long', 
                day: 'numeric'
            });
        }
    }

    exportResults() {
        const sgpa = document.getElementById('sgpaValue')?.textContent || '0.00';
        const percentage = document.getElementById('percentageValue')?.textContent || '0.0%';
        const semester = document.getElementById('semesterSelect').value || 'Not Selected';
        const branch = document.getElementById('branchSelect').value || 'Not Selected';
        const date = new Date().toLocaleDateString('en-IN');

        let report = `VTU SGPA Calculator Report - 2022 Scheme\n`;
        report += `==========================================\n\n`;
        report += `Generated on: ${date}\n`;
        report += `Semester: ${semester === 'lateral' ? 'Lateral Entry' : semester ? `${semester}${this.getOrdinalSuffix(semester)} Semester` : 'Not Selected'}\n`;
        report += `Branch: ${branch ? this.branches[branch] : 'Not Selected'}\n\n`;
        
        report += `RESULTS:\n`;
        report += `SGPA: ${sgpa}/10.0\n`;
        report += `Equivalent Percentage: ${percentage}\n\n`;
        
        report += `COURSE DETAILS:\n`;
        report += `${'Code'.padEnd(10)} ${'Name'.padEnd(35)} ${'Credits'.padEnd(8)} ${'Grade'.padEnd(6)} ${'Points'.padEnd(8)}\n`;
        report += `${'-'.repeat(75)}\n`;

        this.courses.forEach(course => {
            const gradePoints = this.vtuGrading[course.grade]?.points || 0;
            const creditPoints = course.credits * gradePoints;
            report += `${course.code.padEnd(10)} ${course.name.slice(0, 34).padEnd(35)} ${course.credits.toString().padEnd(8)} ${course.grade.padEnd(6)} ${creditPoints.toFixed(1).padEnd(8)}\n`;
        });

        report += `\nVTU SGPA Formula: SGPA = ∑(Ci × Gi) / ∑Ci\n`;
        report += `Where Ci = Credits, Gi = Grade Points\n\n`;
        report += `Disclaimer: This is an unofficial calculator. Please verify with official VTU sources.\n`;

        // Download file
        this.downloadFile(report, `VTU_SGPA_Report_${date.replace(/\//g, '-')}.txt`, 'text/plain');
    }

    printGradeSheet() {
        // Hide non-printable elements temporarily
        const elementsToHide = document.querySelectorAll('.tab-buttons, .action-buttons, .upload-section, .course-input-form, .help-section');
        elementsToHide.forEach(el => el.style.display = 'none');

        // Show only results
        this.switchToTab('results');

        // Print
        window.print();

        // Restore hidden elements
        elementsToHide.forEach(el => el.style.display = '');
    }

    shareResults() {
        const sgpa = document.getElementById('sgpaValue')?.textContent || '0.00';
        const percentage = document.getElementById('percentageValue')?.textContent || '0.0%';
        
        const shareText = `My VTU SGPA: ${sgpa}/10.0 (${percentage}) calculated using VTU 2022 Scheme. Calculate yours at ${window.location.href}`;
        
        if (navigator.share) {
            navigator.share({
                title: 'VTU SGPA Result',
                text: shareText,
                url: window.location.href
            });
        } else {
            // Fallback to copying to clipboard
            navigator.clipboard.writeText(shareText).then(() => {
                this.showStatus('Results copied to clipboard!', 'success');
            });
        }
    }

    resetCalculator() {
        if (confirm('Are you sure you want to reset the calculator? All data will be lost.')) {
            this.courses = [];
            
            // Clear all inputs
            ['courseCode', 'courseName', 'marksInput', 'extractedText'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.value = '';
            });

            // Reset selects
            ['semesterSelect', 'branchSelect', 'courseCredits', 'gradeSelect'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.selectedIndex = 0;
            });

            // Clear tables
            ['courseTableBody', 'gradeSheetBody'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.innerHTML = '';
            });

            // Hide sections
            ['processingSection', 'textPreviewSection', 'courseTableSection'].forEach(id => {
                this.hideSection(id);
            });

            // Switch to first tab
            this.switchToTab('pdf-upload');
            
            // Clear status
            this.clearStatus();
        }
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    showSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove('hidden');
        }
    }

    hideSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('hidden');
        }
    }

    updateProgress(percentage) {
        const progressFill = document.getElementById('progressFill');
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
    }

    showStatus(message, type) {
        const statusEl = document.getElementById('uploadStatus');
        if (statusEl) {
            statusEl.textContent = message;
            statusEl.className = `upload-status ${type}`;
        }
    }

    clearStatus() {
        const statusEl = document.getElementById('uploadStatus');
        if (statusEl) {
            statusEl.textContent = '';
            statusEl.className = 'upload-status';
        }
    }

    showLoading(title, text) {
        const overlay = document.getElementById('loadingOverlay');
        const titleEl = document.getElementById('loadingTitle');
        const textEl = document.getElementById('loadingText');
        
        if (overlay && titleEl && textEl) {
            titleEl.textContent = title;
            textEl.textContent = text;
            overlay.classList.remove('hidden');
        }
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.add('hidden');
        }
    }
}

// Global function for tab switching (called from HTML)
function switchToTab(tabId) {
    if (window.vtuCalculator) {
        window.vtuCalculator.switchToTab(tabId);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.vtuCalculator = new VTUSGPACalculator();
});