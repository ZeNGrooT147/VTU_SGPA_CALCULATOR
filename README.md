# 🎯 Smart VTU SGPA Calculator

**Auto-detects your scheme & branch • Just upload your PDF!**

A revolutionary VTU SGPA calculator that automatically detects your VTU scheme and branch from your transcript PDF, eliminating the need for manual setup.

## ✨ Key Features

### 🎯 **Intelligent Auto-Detection**
- **Automatic Scheme Detection**: Recognizes VTU schemes (2015-2022) from course codes
- **Automatic Branch Detection**: Identifies your branch (CS, EC, ME, CV, EE, IS, AD, BT, CH) from course patterns
- **Smart Course Extraction**: Parses course codes, names, credits, and grades automatically

### 📊 **Multi-Strategy PDF Parsing**
- **Table-based extraction** for structured PDFs
- **Line-by-line text parsing** for unstructured formats
- **Pattern matching** with advanced regex
- **OCR-like processing** for complex layouts

### ⚡ **Instant Results**
- **Real-time SGPA calculation** using correct VTU formulas
- **Grade distribution analysis** with visual charts
- **Performance insights** and predictions
- **Export options** (PDF, Excel)

## 🚀 How It Works

### **Before (Complex Setup)**
```
1. Select VTU Scheme (2015-2022)
2. Choose Branch (50+ options)
3. Select Semester (1-8)
4. Choose Data Entry Method
5. Upload PDF or Manual Entry
6. Calculate SGPA
```

### **Now (Smart Auto-Detection)**
```
1. Upload PDF
2. Get Results Instantly! ✨
```

## 📋 Supported Formats

### **VTU Schemes**
- **2022 Scheme**: BCS101, BEC102, BME103, etc.
- **2021 Scheme**: 21CS11, 21EC12, 21ME13, etc.
- **2018 Scheme**: 18CS11, 18EC12, 18ME13, etc.
- **2017 Scheme**: 17CS11, 17EC12, 17ME13, etc.
- **2015 Scheme**: 15CS11, 15EC12, 15ME13, etc.

### **Branches Supported**
- **Computer Science & Engineering** (CS)
- **Electronics & Communication** (EC)
- **Mechanical Engineering** (ME)
- **Civil Engineering** (CV)
- **Electrical & Electronics** (EE)
- **Information Science** (IS)
- **AI & Data Science** (AD)
- **Biotechnology** (BT)
- **Chemical Engineering** (CH)

## 🛠️ Installation & Setup

### Prerequisites
```bash
Python 3.7+
pip
```

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd vtu-sgpa-calculator

# Install dependencies
pip install -r requirements.txt

# Run the application
python vtu_pdf_parser.py
```

### Access the Application
Open your browser and go to: `http://localhost:5000`

## 📖 Usage

### **Step 1: Upload PDF**
- Drag and drop your VTU transcript PDF
- Or click "Choose PDF File" to browse

### **Step 2: Automatic Processing**
The system will:
- 🔍 Detect your VTU scheme automatically
- 🏫 Identify your branch from course codes
- 📊 Extract all course data
- 🧮 Calculate SGPA using correct formulas

### **Step 3: View Results**
- **SGPA Score** with performance badge
- **Course Details** with grades and credits
- **Grade Distribution** analysis
- **Export Options** for your records

## 🔧 Advanced Features

### **Manual Override (Optional)**
If auto-detection doesn't work perfectly:
1. Click "Advanced: Manual Setup"
2. Select your scheme and branch manually
3. Upload PDF with manual settings

### **Export Options**
- **PDF Export**: Professional grade sheet
- **Excel Export**: Detailed spreadsheet
- **Share Results**: Copy to clipboard or share link

## 🎨 Interface Features

### **Smart Upload Zone**
- Drag & drop support
- Visual feedback on hover
- File type validation

### **Real-time Processing**
- Progress indicators
- Status updates
- Auto-detection results display

### **Responsive Design**
- Works on desktop, tablet, and mobile
- Touch-friendly interface
- Adaptive layouts

## 🧠 Technical Details

### **Auto-Detection Algorithm**
```python
# Scheme Detection
- Pattern matching for course codes
- Confidence scoring system
- Multiple validation checks

# Branch Detection
- Course code prefix analysis
- Frequency counting
- Pattern recognition
```

### **PDF Parsing Strategies**
1. **Table Extraction**: For structured PDFs
2. **Text Parsing**: For unstructured formats
3. **Regex Matching**: For course code patterns
4. **Fallback Processing**: For complex layouts

### **SGPA Calculation**
```python
SGPA = Σ(Credits × Grade Points) / Σ(Credits)
```

## 🎯 Supported Course Patterns

### **2022 Scheme Examples**
- BCS101 (Computer Science)
- BEC102 (Electronics)
- BME103 (Mechanical)
- BCV104 (Civil)

### **2021 Scheme Examples**
- 21CS11 (Computer Science)
- 21EC12 (Electronics)
- 21ME13 (Mechanical)
- 21CV14 (Civil)

### **2018-2015 Schemes**
- 18CS11, 17CS11, 15CS11
- 18EC12, 17EC12, 15EC12
- And many more...

## 🔒 Privacy & Security

- **No Data Storage**: Your PDF is processed in memory only
- **Local Processing**: All calculations happen on your device
- **Secure Upload**: HTTPS encryption for file transfers
- **No Registration**: Use immediately without signup

## 🐛 Troubleshooting

### **Common Issues**

**PDF Not Detecting Courses**
- Ensure it's a VTU transcript PDF
- Check if course codes are visible
- Try manual setup option

**Wrong Scheme Detected**
- Use manual override in advanced settings
- Check course code patterns
- Verify PDF quality

**Processing Errors**
- Check PDF file size (max 10MB)
- Ensure PDF is not password protected
- Try a different PDF format

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This is an **unofficial calculator** for educational purposes. Please verify all calculations with official VTU sources and academic advisors.

---

**Made with ❤️ for VTU Students**

*Simplify your SGPA calculation with intelligent auto-detection!*
