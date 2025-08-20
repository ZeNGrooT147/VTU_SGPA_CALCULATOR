// VTU SGPA Calculator - Frontend JavaScript
class VTUCalculator {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentResults = null;
    }

    initializeElements() {
        // Main sections
        this.uploadSection = document.getElementById('uploadSection');
        this.loadingSection = document.getElementById('loadingSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');

        // Upload elements
        this.uploadArea = document.getElementById('uploadArea');
        this.pdfFileInput = document.getElementById('pdfFile');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.apiKeyInput = document.getElementById('apiKey');
        this.toggleKeyBtn = document.getElementById('toggleKey');

        // Results elements
        this.schemeInfo = document.getElementById('schemeInfo');
        this.branchInfo = document.getElementById('branchInfo');
        this.sgpaInfo = document.getElementById('sgpaInfo');
        this.subjectsTableBody = document.getElementById('subjectsTableBody');
        this.totalSubjects = document.getElementById('totalSubjects');
        this.passedSubjects = document.getElementById('passedSubjects');
        this.totalCredits = document.getElementById('totalCredits');
        this.totalCreditPoints = document.getElementById('totalCreditPoints');

        // Action buttons
        this.newUploadBtn = document.getElementById('newUploadBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.shareBtn = document.getElementById('shareBtn');
        this.retryBtn = document.getElementById('retryBtn');
    }

    bindEvents() {
        // Upload area events
        this.uploadArea.addEventListener('click', () => this.pdfFileInput.click());
        this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
        this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        this.pdfFileInput.addEventListener('change', this.handleFileSelect.bind(this));

        // Button events
        this.uploadBtn.addEventListener('click', this.processPDF.bind(this));
        this.newUploadBtn.addEventListener('click', this.resetToUpload.bind(this));
        this.downloadBtn.addEventListener('click', this.downloadResults.bind(this));
        this.shareBtn.addEventListener('click', this.shareResults.bind(this));
        this.retryBtn.addEventListener('click', this.resetToUpload.bind(this));

        // API key toggle
        this.toggleKeyBtn.addEventListener('click', this.toggleApiKeyVisibility.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0 && files[0].type === 'application/pdf') {
            this.pdfFileInput.files = files;
            this.handleFileSelect();
        }
    }

    handleFileSelect() {
        const file = this.pdfFileInput.files[0];
        if (file) {
            this.uploadArea.classList.add('file-selected');
            this.uploadArea.querySelector('.upload-text p').textContent = file.name;
            this.uploadBtn.disabled = false;
        }
    }

    toggleApiKeyVisibility() {
        const type = this.apiKeyInput.type === 'password' ? 'text' : 'password';
        this.apiKeyInput.type = type;
        this.toggleKeyBtn.innerHTML = type === 'password' ? '<i class="fas fa-eye"></i>' : '<i class="fas fa-eye-slash"></i>';
    }

    async processPDF() {
        const file = this.pdfFileInput.files[0];
        if (!file) return;

        try {
            this.showLoading();
            
            // Convert PDF to base64
            const base64Content = await this.fileToBase64(file);
            
            // Prepare request data
            const requestData = {
                pdf_content: base64Content,
                api_key: this.apiKeyInput.value.trim()
            };

            // Make API call to Vercel function
            const response = await fetch('/api/parse_pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                this.currentResults = result;
                this.displayResults(result);
            } else {
                throw new Error(result.error || 'Failed to process PDF');
            }

        } catch (error) {
            console.error('Error processing PDF:', error);
            this.showError(error.message);
        }
    }

    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    displayResults(results) {
        // Update scheme and branch info
        this.schemeInfo.textContent = results.scheme;
        this.branchInfo.textContent = this.getBranchFullName(results.branch);
        this.sgpaInfo.textContent = `SGPA: ${results.sgpa}`;

        // Populate subjects table
        this.populateSubjectsTable(results.subjects);

        // Update summary stats
        this.updateSummaryStats(results.summary);

        // Show results section
        this.showResults();
    }

    populateSubjectsTable(subjects) {
        this.subjectsTableBody.innerHTML = '';
        
        subjects.forEach(subject => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${subject.code}</td>
                <td>${subject.name}</td>
                <td class="marks internal">${subject.internal}</td>
                <td class="marks external">${subject.external}</td>
                <td class="marks total">${subject.total}</td>
                <td class="result ${subject.result === 'P' ? 'pass' : 'fail'}">${subject.result}</td>
                <td class="credits">${subject.credits}</td>
                <td class="grade">${subject.grade}</td>
                <td class="grade-points">${subject.grade_point}</td>
                <td class="credit-points">${subject.credit_points}</td>
            `;
            this.subjectsTableBody.appendChild(row);
        });
    }

    updateSummaryStats(summary) {
        this.totalSubjects.textContent = summary.total_subjects;
        this.passedSubjects.textContent = summary.passed_subjects;
        this.totalCredits.textContent = summary.total_credits;
        this.totalCreditPoints.textContent = summary.total_credit_points;
    }

    getBranchFullName(branchCode) {
        const branchNames = {
            'CS': 'Computer Science',
            'EC': 'Electronics & Communication',
            'ME': 'Mechanical',
            'CV': 'Civil',
            'EE': 'Electrical',
            'IS': 'Information Science',
            'AD': 'Aerospace',
            'BT': 'Biotechnology',
            'CH': 'Chemical'
        };
        return branchNames[branchCode] || branchCode;
    }

    showLoading() {
        this.uploadSection.style.display = 'none';
        this.loadingSection.style.display = 'block';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    showResults() {
        this.uploadSection.style.display = 'none';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'block';
        this.errorSection.style.display = 'none';
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        this.uploadSection.style.display = 'none';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'block';
    }

    resetToUpload() {
        // Reset file input
        this.pdfFileInput.value = '';
        this.uploadBtn.disabled = true;
        this.uploadArea.classList.remove('file-selected');
        this.uploadArea.querySelector('.upload-text p').textContent = 'Click to select PDF or drag & drop here';
        
        // Clear API key
        this.apiKeyInput.value = '';
        
        // Show upload section
        this.uploadSection.style.display = 'block';
        this.loadingSection.style.display = 'none';
        this.resultsSection.style.display = 'none';
        this.errorSection.style.display = 'none';
    }

    downloadResults() {
        if (!this.currentResults) return;

        const data = {
            timestamp: new Date().toISOString(),
            scheme: this.currentResults.scheme,
            branch: this.currentResults.branch,
            sgpa: this.currentResults.sgpa,
            subjects: this.currentResults.subjects,
            summary: this.currentResults.summary
        };

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `vtu_results_${this.currentResults.scheme}_${this.currentResults.branch}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    async shareResults() {
        if (!this.currentResults) return;

        const shareText = `VTU Results - ${this.currentResults.scheme} Scheme, ${this.currentResults.branch} Branch\nSGPA: ${this.currentResults.sgpa}\nTotal Credits: ${this.currentResults.summary.total_credits}`;

        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'VTU SGPA Results',
                    text: shareText
                });
            } catch (error) {
                console.log('Share cancelled or failed');
            }
        } else {
            // Fallback: copy to clipboard
            try {
                await navigator.clipboard.writeText(shareText);
                this.showToast('Results copied to clipboard!');
            } catch (error) {
                console.error('Failed to copy to clipboard:', error);
            }
        }
    }

    showToast(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        document.body.appendChild(toast);

        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);

        // Hide and remove toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
}

// Initialize the calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VTUCalculator();
});

// Add toast styles
const style = document.createElement('style');
style.textContent = `
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4CAF50;
        color: white;
        padding: 12px 24px;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        z-index: 1000;
    }
    
    .toast.show {
        transform: translateX(0);
    }
    
    .drag-over {
        border-color: #4CAF50 !important;
        background-color: rgba(76, 175, 80, 0.1) !important;
    }
    
    .file-selected {
        border-color: #2196F3 !important;
        background-color: rgba(33, 150, 243, 0.1) !important;
    }
    
    .file-selected .upload-text p {
        color: #2196F3 !important;
    }
`;
document.head.appendChild(style);