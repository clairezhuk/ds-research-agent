from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .analyze_service import analyze_text
from .search_news_service import search_news

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
    news = search_news(count)
    return {"news": news}

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
    result = await analyze_text(text)
    return {"result": result}