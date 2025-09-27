from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news")
def get_news(count: int = Query(2, ge=1)):
    all_news = [
        ["Test News 1", "Description 1", "https://example.com/1"],
        ["Test News 2", "Description 2", "https://example.com/2"],
        ["Test News 3", "Description 3", "https://example.com/3"],
        ["Test News 4", "Description 4", "https://example.com/4"],
    ]
    return {"news": all_news[:count]}

@app.get("/jobs")
def get_jobs(count: int = Query(2, ge=1)):
    jobs = [
        ["AI Engineer", "Work on ML models at Company X"],
        ["Data Scientist", "Analyze data at Company Y"],
        ["Research Intern", "Assist in AI research at Lab Z"],
        ["ML Ops", "Deploy ML pipelines at Company Q"],
    ]
    return {"jobs": jobs[:count]}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")
    return {"result": f"Test analysis of: {text[:30]}..."}
