import fastapi
import uvicorn
from utils import job_desc_score, cv_score

app = fastapi.FastAPI()

@app.post("/job_desc_score/")
async def job_desc_score_endpoint(data: dict):
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    print(job_title, job_description)
    if job_title is None or job_description is None:
        return {"error": "Both job_title and job_description are required."}
    
    result = job_desc_score(job_title, job_description)
    return result

@app.post("/cv_rank_endpoint/")
async def cv_rank_endpoint(data: dict):
    job_title = data.get('job_title')
    list_cv_texts = data.get('list_cv_texts')
    if job_title is None or list_cv_texts is None:
        return {"error": "Both job_title and job_description are required."}
    result = list_cv_texts(job_title, list_cv_texts)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)