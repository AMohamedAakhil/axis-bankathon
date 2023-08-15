import fastapi
import asyncio
import uvicorn

from utils.job_desc_llm import JobDescLLM
from utils.cv_llm import CVranker
from utils.interview_llm import InterviewLLM

app = fastapi.FastAPI()


@app.post("/job_desc_score/")
async def job_desc_score_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')

    job_llm = JobDescLLM(job_title=job_title, 
                         job_description=job_description)
    
    if job_title is None or job_description is None:
        return {"error": "Both job_title and job_description are required."}
    
    
    score, element_wise_score, enhancement_recc, edited_job_description = await job_llm.generate_concurrently()
    return score, element_wise_score, enhancement_recc, edited_job_description

@app.post("/cv_ranking/")
async def cv_ranking_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    cv_links = data.get('cv_links')

    cv_ranker = CVranker(job_title=job_title, 
                         job_description=job_description,
                         cv_links_list=cv_links)
    
    cv_rankings = await cv_ranker.generate_rankings()
    return cv_rankings

@app.post("/interview_questions/")
async def interview_questions_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    cv= data.get('cv')

    interview_llm = InterviewLLM(job_title=job_title, 
                         job_description=job_description,
                         cv=cv)
    
    questions = interview_llm.generate_questions()
    return questions

@app.post("/evaluate_qna/")
async def evaluate_qna_endpoint(data: dict):
    job_title = data.get('job_title')
    question = data.get('questions')
    answer = data.get('answers')

    score_per_question, total_score = await InterviewLLM.evaluate_answers(job_title=job_title,
                                         question=question,
                                         answer=answer)
    return score_per_question, total_score


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)