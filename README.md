# AI HR Assistant - Streamlit App

A modern, AI-powered HR application built with Streamlit that uses Google's Gemini AI to analyze and rank CVs based on job requirements.

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your Gemini API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run the app
streamlit run streamlit_app.py
```

## ✨ Features

- 📄 **PDF CV Upload**: Upload multiple PDF CVs for analysis
- 🤖 **AI-Powered Analysis**: Uses Gemini AI to analyze CVs against job requirements
- 📊 **Comprehensive Scoring**: Scores CVs across 9 key dimensions
- 🏆 **Smart Ranking**: Automatically ranks candidates by total score
- 📈 **Detailed Reports**: View detailed analysis for each CV
- 📤 **Export Results**: Download results as CSV for further analysis

## 🏗️ Architecture

- **Frontend**: Streamlit (Python-based web framework)
- **AI Engine**: Google Gemini Pro API
- **PDF Processing**: PyPDF2 for text extraction
- **Data Analysis**: Pandas for data manipulation and export
- **Evaluation Criteria**: Based on industry-standard CV elements from `cv_elements.json`

## 📁 Project Structure

```
├── streamlit_app.py          # Main Streamlit application
├── demo_cv_analysis.py       # Demo script for testing
├── setup.py                  # Automated setup script
├── run_app.py                # Quick start runner
├── requirements.txt          # Python dependencies
├── README_STREAMLIT.md      # Detailed documentation
├── .streamlit/config.toml   # Streamlit configuration
└── src/server/py_utils/json_components/
    ├── cv_elements.json     # CV evaluation criteria
    └── jd_elements.json    # Job description elements
```

## 🔧 Configuration

1. **Get Gemini API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Set Environment Variable**: Add your API key to `.env` file
3. **Customize Evaluation**: Modify `cv_elements.json` to adjust scoring criteria

## 📖 Documentation

- **Setup Guide**: See `README_STREAMLIT.md` for detailed instructions
- **Demo**: Run `python demo_cv_analysis.py` to test functionality
- **Configuration**: Check `.streamlit/config.toml` for app settings

## 🔄 Migration from Previous Version

This Streamlit app replaces the previous TypeScript/Next.js + FastAPI setup:

- ✅ **Removed**: TypeScript/Next.js frontend
- ✅ **Removed**: FastAPI backend  
- ✅ **Removed**: OpenAI API dependency
- ✅ **Added**: Streamlit frontend
- ✅ **Added**: Google Gemini API integration
- ✅ **Maintained**: CV evaluation logic and criteria
- ✅ **Enhanced**: Better UI/UX with Streamlit components

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.


