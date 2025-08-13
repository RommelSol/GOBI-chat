from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.gobi_core import build_index, infer_paths_from_dir, retrieve, compose_answer
from app.emotion import detect_emotion, empathetic_prefix

app = FastAPI(title="GOBI Web")
app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

# Construye índice una vez al iniciar
DOC_INDEX = build_index(infer_paths_from_dir())

class AskPayload(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
def ask(payload: AskPayload):
    q = (payload.query or "").strip()
    if not q:
        return JSONResponse({"answer": "Escribe una consulta.", "sources": []})
    emo = detect_emotion(q)
    hits = retrieve(q, DOC_INDEX)
    result = compose_answer(q, hits)
    answer = empathetic_prefix(emo) + result["answer"]
    return JSONResponse({"answer": answer, "sources": result["sources"]})