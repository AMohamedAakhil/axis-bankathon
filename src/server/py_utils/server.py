import fastapi
import uvicorn
import os

import smtplib
from email.message import EmailMessage
import ssl

from dotenv import load_dotenv
from os.path import join, dirname

from utils.job_desc_llm import JobDescLLM
from utils.cv_llm import CVranker
from utils.interview_llm import InterviewLLM

app = fastapi.FastAPI()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EMAIL_PASS = os.environ.get("EMAIL_PASS")

@app.post("/job_desc_score/")
async def job_desc_score_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')

    job_llm = JobDescLLM(job_title=job_title, 
                         job_description=job_description)
    
    if job_title is None or job_description is None:
        return {"error": "Both job_title and job_description are required."}
    

    try:
        score, element_wise_score, enhancement_recc, edited_job_description = await job_llm.generate_concurrently()
        return score, element_wise_score, enhancement_recc, edited_job_description
    except ValueError:
            return "We ran into an unexpected error, Please try again"


@app.post("/cv_ranking/")
async def cv_ranking_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    cv_links = data.get('cv_links')

    cv_ranker = CVranker(job_title=job_title, 
                         job_description=job_description,
                         cv_links_list=cv_links)
    
    try:
        cv_rankings = await cv_ranker.generate_rankings()
        return cv_rankings
    except ValueError:
        return "We ran into an unexpected error, Please try again"
        

@app.post("/interview_questions/")
async def interview_questions_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    cv= data.get('cv')

    interview_llm = InterviewLLM(job_title=job_title, 
                         job_description=job_description,
                         cv=cv)
    

    try:
        questions = interview_llm.generate_questions()
        return questions
    except ValueError:
        return "We ran into an unexpected error, Please try again"

@app.post("/evaluate_qna/")
async def evaluate_qna_endpoint(data: dict):
    job_title = data.get('job_title')
    question = data.get('questions')
    answer = data.get('answers')

    try:

        score_per_question, total_score = await InterviewLLM.evaluate_answers(job_title=job_title,
                                         question=question,
                                         answer=answer)
        return score_per_question, total_score
    except ValueError:
        return "We ran into an unexpected error, Please try again"
    
@app.post("/evaluate_qna/")
async def evaluate_qna_endpoint(data: dict):
    job_title = data.get('job_title')
    question = data.get('questions')
    answer = data.get('answers')

    try:

        score_per_question, total_score = await InterviewLLM.evaluate_answers(job_title=job_title,
                                         question=question,
                                         answer=answer)
        return score_per_question, total_score
    except ValueError:
        return "We ran into an unexpected error, Please try again"
    
@app.post("/send_round1_email/")
def send_round1_mail(data):
    email_sender = 'axisbank.hrteam123@gmail.com'
    email_password = EMAIL_PASS
    email_receiver = data.get('receiver_email')
    interview_link = data.get('interview_link')

    subject = 'Congratulations on Your Selection for an Round 1 Interview at Axis Bank!'
    body =f"""
    Dear Candidate,
    We are thrilled to inform you that after a thorough review of your application, we are impressed with your qualifications and experiences,
    and we would like to invite you for an interview at Axis Bank.
    Your application stood out among a competitive pool of candidates, and we believe your skills and background align well with what we are looking
    for in this position.
    
    Interview Details:
    Mode: Online
    Link: {interview_link}
    
    Best regards,

    Axis Bank
    HR admin
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    response={
        "sent" : "true",
    }
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)