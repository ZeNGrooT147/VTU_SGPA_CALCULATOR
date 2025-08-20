# VTU SGPA Calculator - Vercel Deployment Guide

## 🚀 Deploy to Vercel

This VTU SGPA Calculator has been optimized for Vercel serverless deployment with AI-powered PDF parsing capabilities.

## 📁 Project Structure

```
├── api/
│   └── parse_pdf.py          # Serverless API function
├── public/
│   ├── index.html            # Main frontend
│   ├── style.css             # Styling
│   └── app.js                # Frontend logic
├── subjects_database.py      # VTU subjects database
├── requirements.txt          # Python dependencies
├── vercel.json              # Vercel configuration
└── README_VERCEL.md         # This file
```

## 🛠️ Features

- **AI-Powered PDF Parsing**: Uses Google Gemini AI for intelligent result extraction
- **Auto-Detection**: Automatically detects VTU scheme (2022, 2021, 2018) and branch
- **Comprehensive Database**: Complete VTU subjects database with accurate credits
- **Real-time SGPA Calculation**: Instant SGPA calculation with detailed breakdown
- **Modern UI**: Beautiful, responsive interface with drag & drop PDF upload
- **Serverless Architecture**: Built for Vercel with optimized performance

## 🚀 Quick Deploy

### Option 1: Deploy with Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Follow the prompts** and your app will be deployed!

### Option 2: Deploy via Vercel Dashboard

1. **Push to GitHub**: Upload your code to a GitHub repository
2. **Connect to Vercel**: Go to [vercel.com](https://vercel.com) and import your repo
3. **Deploy**: Vercel will automatically detect the Python project and deploy it

## 🔧 Environment Variables

### Required (Optional for AI features):
- `GEMINI_API_KEY`: Your Google Gemini API key for enhanced PDF parsing

### How to set:
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add `GEMINI_API_KEY` with your API key value

## 📊 API Endpoints

### POST `/api/parse_pdf`
Processes VTU result PDFs and returns structured data.

**Request Body**:
```json
{
  "pdf_content": "base64_encoded_pdf",
  "api_key": "your_gemini_api_key_optional"
}
```

**Response**:
```json
{
  "success": true,
  "subjects": [...],
  "scheme": "2022",
  "branch": "CS",
  "sgpa": 8.45,
  "summary": {...}
}
```

## 🎯 How It Works

1. **PDF Upload**: Users drag & drop or select VTU result PDFs
2. **AI Processing**: Gemini AI extracts subject data with high accuracy
3. **Fallback Parsing**: Traditional regex parsing if AI fails
4. **Database Lookup**: Matches subjects with comprehensive VTU database
5. **SGPA Calculation**: Calculates accurate SGPA using VTU grading system
6. **Results Display**: Beautiful table with all subject details and summary

## 🔍 Supported VTU Schemes

- **2022 Scheme**: Latest VTU curriculum with comprehensive subject coverage
- **2021 Scheme**: Previous year curriculum
- **2018 Scheme**: Legacy curriculum support

## 🏗️ Architecture

- **Frontend**: Vanilla JavaScript with modern CSS
- **Backend**: Python serverless functions on Vercel
- **AI Integration**: Google Gemini Vision API
- **Database**: Comprehensive VTU subjects database
- **Parsing**: Dual approach (AI + Traditional regex)

## 📱 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🚨 Limitations

- **File Size**: PDFs must be under Vercel's function size limits
- **Processing Time**: Maximum 30 seconds per request (configurable in vercel.json)
- **API Rate Limits**: Subject to Gemini API rate limits

## 🔧 Customization

### Modify Subjects Database
Edit `subjects_database.py` to add/update VTU subjects and credits.

### Update Grading Schemes
Modify the `VTU_SCHEMES` dictionary in `api/parse_pdf.py` for different grading systems.

### Customize UI
Modify files in the `public/` directory to customize the frontend appearance.

## 🐛 Troubleshooting

### Common Issues:

1. **Function Timeout**: Increase `maxDuration` in `vercel.json`
2. **PDF Not Processing**: Check if PDF is valid and readable
3. **AI Parsing Fails**: Verify Gemini API key and quota
4. **CORS Errors**: CORS is already configured in the API

### Debug Mode:
Check Vercel function logs in your dashboard for detailed error information.

## 📈 Performance

- **Cold Start**: ~2-3 seconds for first request
- **Warm Start**: ~500ms for subsequent requests
- **PDF Processing**: 5-15 seconds depending on complexity
- **AI Processing**: 3-8 seconds with Gemini API

## 🔒 Security

- **Input Validation**: All PDF inputs are validated
- **API Key Protection**: Gemini API key is not exposed to frontend
- **CORS**: Configured for production use
- **Rate Limiting**: Built-in protection against abuse

## 📞 Support

For issues or questions:
1. Check Vercel function logs
2. Verify environment variables
3. Test with sample PDFs
4. Check Gemini API status

## 🎉 Success!

Once deployed, your VTU SGPA Calculator will be available at:
`https://your-project-name.vercel.app`

The app automatically scales with traffic and provides a professional-grade VTU result processing experience!
