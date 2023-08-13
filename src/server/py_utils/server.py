import fastapi
import asyncio
import uvicorn
from utils import JobDescLLM

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)