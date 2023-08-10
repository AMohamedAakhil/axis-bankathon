import fastapi  
from utils import job_desc_score

app = fastapi.FastAPI()

@app.get("/job_desc_score")
async def job_desc_score_endpoint(job_title: str, job_description: str):
    """Score a job description and return a list with the score and potential enhancements."""
    return eval(job_desc_score(job_title, job_description))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)