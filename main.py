from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz, QuizResponse
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from schemas import TextRequest, QAResponse, TextResponse, LearningPathResponse

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant based on the supplied project specification.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa", response_model=QAResponse)
async def qa(payload: TextRequest):
    try:
        answer = await answer_question(payload.text)
        return QAResponse(answer=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/explain", response_model=TextResponse)
async def explain(payload: TextRequest):
    try:
        answer = await explain_concept(payload.text)
        return TextResponse(result=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TextRequest):
    try:
        return await generate_quiz(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/summarize", response_model=TextResponse)
async def summarize(payload: TextRequest):
    try:
        answer = await summarize_text(payload.text)
        return TextResponse(result=answer)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/learn/recommendations", response_model=LearningPathResponse)
async def learning_recommendations(payload: TextRequest):
    try:
        return await get_learning_recommendations(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
