import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import json
import pandas as pd
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("Please set GOOGLE_API_KEY in your .env file")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Load CV evaluation criteria
def load_cv_elements():
    with open("cv_elements.json", "r") as f:
        return json.load(f)

def load_jd_elements():
    with open("jd_elements.json", "r") as f:
        return json.load(f)

# PDF text extraction
def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# CV Analysis using Gemini
def analyze_cv_with_gemini(cv_text: str, job_title: str, job_description: str, cv_elements: Dict) -> Dict[str, Any]:
    """Analyze CV using Gemini API and return structured analysis"""
    
    prompt = f"""
    You are an HR expert analyzing a CV for the position of {job_title}.
    
    Job Description:
    {job_description}
    
    CV Content:
    {cv_text}
    
    Please analyze the CV and provide the following information in JSON format:
    
    For each of these CV elements, identify the relevant content and score it out of 10:
    {json.dumps(cv_elements, indent=2)}
    
    Return ONLY a valid JSON object with this structure:
    {{
        "Contact Information": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Summary/Objective": {{
            "content": "extracted content or null if not found", 
            "score": "score out of 10"
        }},
        "Work Experience": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Education": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Skills": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Achievements": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Projects/Portfolio": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Certifications": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }},
        "Languages": {{
            "content": "extracted content or null if not found",
            "score": "score out of 10"
        }}
    }}
    
    Be strict in scoring. Only give high scores (8-10) for excellent matches, medium scores (5-7) for good matches, and low scores (1-4) for poor matches.
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from response
        response_text = response.text
        # Find JSON content between ```json and ``` or just parse the response
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_content = response_text[json_start:json_end].strip()
        else:
            json_content = response_text.strip()
        
        analysis = json.loads(json_content)
        return analysis
    except Exception as e:
        st.error(f"Error analyzing CV with Gemini: {e}")
        return {}

def calculate_total_score(analysis: Dict[str, Any]) -> float:
    """Calculate total score from CV analysis"""
    total_score = 0
    for element, data in analysis.items():
        if isinstance(data, dict) and 'score' in data:
            try:
                score = float(data['score'])
                total_score += score
            except (ValueError, TypeError):
                continue
    return total_score

def generate_cv_summary(cv_text: str) -> str:
    """Generate a concise summary of the CV"""
    prompt = f"""
    Summarize this CV in 2-3 sentences, highlighting the key qualifications and experience:
    
    {cv_text}
    
    Return only the summary, no additional text.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {e}"

# Streamlit UI
def main():
    st.set_page_config(
        page_title="AI HR Assistant - CV Ranking",
        page_icon="👔",
        layout="wide"
    )
    
    st.title("👔 AI HR Assistant - CV Ranking System")
    st.markdown("Upload CVs and get AI-powered ranking based on job requirements")
    
    # Load evaluation criteria
    cv_elements = load_cv_elements()
    jd_elements = load_jd_elements()
    
    # Sidebar for job details
    with st.sidebar:
        st.header("Job Details")
        job_title = st.text_input("Job Title", placeholder="e.g., Software Engineer")
        job_description = st.text_area("Job Description", 
                                     placeholder="Enter the job description here...",
                                     height=200)
        
        st.markdown("---")
        st.markdown("### CV Evaluation Criteria")
        for element, description in cv_elements.items():
            with st.expander(element):
                st.write(description)
    
    # Main content area
    if not job_title or not job_description:
        st.warning("Please enter both job title and job description in the sidebar to proceed.")
        return
    
    # File upload section
    st.header("Upload CVs")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload multiple PDF CVs for comparison"
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} CV(s)")
        
        # Analysis button
        if st.button("🚀 Analyze and Rank CVs", type="primary"):
            with st.spinner("Analyzing CVs with AI..."):
                cv_rankings = []
                
                for i, uploaded_file in enumerate(uploaded_files):
                    st.write(f"Analyzing CV {i+1}: {uploaded_file.name}")
                    
                    # Extract text from PDF
                    cv_text = extract_text_from_pdf(uploaded_file)
                    
                    if cv_text:
                        # Analyze CV with Gemini
                        analysis = analyze_cv_with_gemini(cv_text, job_title, job_description, cv_elements)
                        
                        if analysis:
                            # Calculate total score
                            total_score = calculate_total_score(analysis)
                            
                            # Generate summary
                            summary = generate_cv_summary(cv_text)
                            
                            # Store results
                            cv_rankings.append({
                                'filename': uploaded_file.name,
                                'total_score': total_score,
                                'analysis': analysis,
                                'summary': summary,
                                'cv_text': cv_text[:500] + "..." if len(cv_text) > 500 else cv_text
                            })
                
                # Sort by total score (descending)
                cv_rankings.sort(key=lambda x: x['total_score'], reverse=True)
                
                # Display results
                st.header("📊 CV Rankings")
                
                # Summary table
                summary_data = []
                for i, ranking in enumerate(cv_rankings):
                    summary_data.append({
                        'Rank': i + 1,
                        'Candidate': ranking['filename'],
                        'Total Score': f"{ranking['total_score']:.1f}/90",
                        'Percentage': f"{(ranking['total_score']/90)*100:.1f}%"
                    })
                
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df, use_container_width=True)
                
                # Detailed analysis for each CV
                for i, ranking in enumerate(cv_rankings):
                    with st.expander(f"📋 {ranking['filename']} - Rank {i+1} (Score: {ranking['total_score']:.1f}/90)"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.subheader("AI Analysis Summary")
                            st.write(ranking['summary'])
                            
                            st.subheader("Detailed Scores")
                            scores_data = []
                            for element, data in ranking['analysis'].items():
                                if isinstance(data, dict) and 'score' in data:
                                    scores_data.append({
                                        'Element': element,
                                        'Score': f"{data['score']}/10",
                                        'Content': data.get('content', 'Not found')[:100] + "..." if data.get('content') and len(str(data.get('content', ''))) > 100 else (data.get('content') or 'Not found')
                                    })
                            
                            scores_df = pd.DataFrame(scores_data)
                            st.dataframe(scores_df, use_container_width=True)
                        
                        with col2:
                            st.subheader("CV Preview")
                            st.text_area("First 500 characters:", ranking['cv_text'], height=200, disabled=True)
                            
                            # Download button for full CV text
                            st.download_button(
                                label="📥 Download Full CV Text",
                                data=ranking['cv_text'],
                                file_name=f"{ranking['filename']}_text.txt",
                                mime="text/plain"
                            )
                
                # Export results
                st.header("📤 Export Results")
                
                # Export to CSV
                export_data = []
                for ranking in cv_rankings:
                    row = {
                        'Filename': ranking['filename'],
                        'Total_Score': ranking['total_score'],
                        'Percentage': (ranking['total_score']/90)*100
                    }
                    
                    # Add individual element scores
                    for element, data in ranking['analysis'].items():
                        if isinstance(data, dict) and 'score' in data:
                            row[f'{element}_Score'] = data['score']
                            row[f'{element}_Content'] = data.get('content', 'Not found')
                    
                    export_data.append(row)
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Results CSV",
                    data=csv,
                    file_name="cv_rankings_results.csv",
                    mime="text/csv"
                )
    
    else:
        st.info("👆 Please upload PDF CVs to get started with the analysis.")

if __name__ == "__main__":
    main() 