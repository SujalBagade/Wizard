# backend/app/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
# Fix imports to be package-relative
from app.models import Problem, Submission
from app.crud import create_problem, get_problem, list_problems, create_submission
from app.ai_client import generate_mcq
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# Update database path for Docker environment
SQLITE_DB_PATH = "/data/wizard.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{SQLITE_DB_PATH}")
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

app = FastAPI(title="Wizard Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    # seed one problem if none
    with Session(engine) as s:
        q = s.exec(text("SELECT COUNT(*) FROM problem")).one_or_none()
        try:
            if q is None or q == 0:
                p = generate_mcq("Physics", "Kinematics", "Easy", seed=42)
                create_problem(s, p)
        except Exception:
            pass

@app.get("/problems")
def api_list_problems(subject: str = None, topic: str = None):
    with Session(engine) as s:
        ps = list_problems(s, subject, topic)
        return {"count": len(ps), "results": [p.dict() for p in ps]}

@app.get("/problems/{problem_id}")
def api_get_problem(problem_id: int):
    with Session(engine) as s:
        p = get_problem(s, problem_id)
        if not p:
            raise HTTPException(status_code=404, detail="Problem not found")
        return p

@app.post("/generate")
def api_generate(subject: str = "Physics", topic: str = "Kinematics", difficulty: str = "Medium"):
    payload = generate_mcq(subject, topic, difficulty)
    with Session(engine) as s:
        p = create_problem(s, payload)
        p.options = json.loads(p.options) if isinstance(p.options, str) else p.options
        return p

@app.post("/submissions")
def api_submit(data: dict):
    with Session(engine) as s:
        s_obj = create_submission(s, data)
        return s_obj
