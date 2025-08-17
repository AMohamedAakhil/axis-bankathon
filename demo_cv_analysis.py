#!/usr/bin/env python3
"""
Demo script for CV analysis functionality
This script demonstrates the core CV analysis logic without the Streamlit UI
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("❌ Please set GOOGLE_API_KEY in your .env file")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def load_cv_elements():
    """Load CV evaluation criteria"""
    with open("cv_elements.json", "r") as f:
        return json.load(f)

def analyze_cv_demo(cv_text: str, job_title: str, job_description: str):
    """Demo CV analysis using Gemini API"""
    
    cv_elements = load_cv_elements()
    
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
        response_text = response.text
        
        # Extract JSON from response
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_content = response_text[json_start:json_end].strip()
        else:
            json_content = response_text.strip()
        
        analysis = json.loads(json_content)
        return analysis
    except Exception as e:
        print(f"❌ Error analyzing CV: {e}")
        return {}

def calculate_total_score(analysis):
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

def main():
    print("🎯 CV Analysis Demo")
    print("=" * 50)
    
    # Sample CV text (you can replace this with actual CV content)
    sample_cv = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | +1-555-0123 | New York, NY
    
    SUMMARY
    Experienced software engineer with 5+ years developing web applications using Python, JavaScript, and React. Passionate about clean code and user experience.
    
    WORK EXPERIENCE
    Senior Software Engineer - Tech Corp (2020-Present)
    - Led development of customer portal application
    - Mentored junior developers and conducted code reviews
    - Improved application performance by 40%
    
    Software Engineer - Startup Inc (2018-2020)
    - Developed RESTful APIs using Python Flask
    - Collaborated with cross-functional teams
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2018
    GPA: 3.8/4.0
    
    SKILLS
    Programming: Python, JavaScript, React, Node.js, SQL
    Tools: Git, Docker, AWS, Jenkins
    Soft Skills: Leadership, Communication, Problem-solving
    
    CERTIFICATIONS
    AWS Certified Developer Associate
    Google Cloud Professional Developer
    
    LANGUAGES
    English (Native), Spanish (Conversational)
    """
    
    # Sample job description
    sample_job = """
    We are looking for a Senior Software Engineer to join our team. The ideal candidate should have:
    - 3+ years of experience in software development
    - Proficiency in Python and JavaScript
    - Experience with React and modern web frameworks
    - Strong problem-solving skills
    - Experience with cloud platforms (AWS/GCP)
    - Bachelor's degree in Computer Science or related field
    """
    
    print("📋 Sample CV:")
    print(sample_cv[:200] + "...")
    print("\n💼 Sample Job Description:")
    print(sample_job[:200] + "...")
    print("\n" + "=" * 50)
    
    print("\n🤖 Analyzing CV with Gemini AI...")
    
    # Analyze the CV
    analysis = analyze_cv_demo(sample_cv, "Senior Software Engineer", sample_job)
    
    if analysis:
        print("\n✅ Analysis Complete!")
        print("\n📊 Results:")
        
        # Calculate total score
        total_score = calculate_total_score(analysis)
        print(f"\n🏆 Total Score: {total_score:.1f}/90 ({total_score/90*100:.1f}%)")
        
        # Display element-wise scores
        print("\n📈 Element-wise Scores:")
        for element, data in analysis.items():
            if isinstance(data, dict) and 'score' in data:
                score = data.get('score', 'N/A')
                content = data.get('content', 'Not found')
                print(f"  {element}: {score}/10")
                if content and content != 'Not found':
                    print(f"    Content: {content[:100]}{'...' if len(str(content)) > 100 else ''}")
        
        # Save results to file
        results = {
            'total_score': total_score,
            'percentage': total_score/90*100,
            'analysis': analysis
        }
        
        with open('demo_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to 'demo_results.json'")
        
    else:
        print("❌ Analysis failed. Please check your API key and try again.")

if __name__ == "__main__":
    main() 