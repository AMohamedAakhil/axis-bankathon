# AI HR Assistant - Streamlit App

A modern HR application built with Streamlit that uses Google's Gemini AI to analyze and rank CVs based on job requirements.

## Features

- 📄 **PDF CV Upload**: Upload multiple PDF CVs for analysis
- 🤖 **AI-Powered Analysis**: Uses Gemini AI to analyze CVs against job requirements
- 📊 **Comprehensive Scoring**: Scores CVs across 9 key dimensions:
  - Contact Information
  - Summary/Objective
  - Work Experience
  - Education
  - Skills
  - Achievements
  - Projects/Portfolio
  - Certifications
  - Languages
- 🏆 **Smart Ranking**: Automatically ranks candidates by total score
- 📈 **Detailed Reports**: View detailed analysis for each CV
- 📤 **Export Results**: Download results as CSV for further analysis

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the root directory:

```bash
# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# Optional: Streamlit configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### 3. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

### 4. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter Job Details**: Fill in the job title and description in the sidebar
2. **Upload CVs**: Upload multiple PDF CVs using the file uploader
3. **Analyze**: Click "Analyze and Rank CVs" to start AI analysis
4. **Review Results**: View rankings, detailed scores, and analysis
5. **Export**: Download results as CSV for further processing

## Architecture

- **Frontend**: Streamlit (Python-based web framework)
- **AI Engine**: Google Gemini Pro API
- **PDF Processing**: PyPDF2 for text extraction
- **Data Analysis**: Pandas for data manipulation and export
- **Evaluation Criteria**: Based on industry-standard CV elements

## File Structure

```
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README_STREAMLIT.md      # This file
├── .env                     # Environment variables (create this)
└── src/server/py_utils/json_components/
    ├── cv_elements.json     # CV evaluation criteria
    └── jd_elements.json    # Job description elements
```

## Scoring System

Each CV element is scored out of 10:
- **8-10**: Excellent match
- **5-7**: Good match  
- **1-4**: Poor match

Total score is calculated as the sum of all element scores (maximum 90 points).

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GOOGLE_API_KEY` is set in your `.env` file
2. **PDF Reading Error**: Ensure PDFs are not corrupted or password-protected
3. **Memory Issues**: For large PDFs, consider splitting them into smaller files

### Performance Tips

- Upload PDFs one at a time for better performance
- Keep job descriptions concise but detailed
- Close other applications to free up memory

## Migration from Previous Version

This Streamlit app replaces the previous TypeScript/Next.js + FastAPI setup:

- ✅ **Removed**: TypeScript/Next.js frontend
- ✅ **Removed**: FastAPI backend
- ✅ **Removed**: OpenAI API dependency
- ✅ **Added**: Streamlit frontend
- ✅ **Added**: Google Gemini API integration
- ✅ **Maintained**: CV evaluation logic and criteria
- ✅ **Enhanced**: Better UI/UX with Streamlit components

## Contributing

Feel free to submit issues and enhancement requests! 