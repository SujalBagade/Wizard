from sqlmodel import Session, select
from .models import Problem, Submission
from typing import List
import json

def create_problem(session: Session, data: dict) -> Problem:
    data2 = data.copy()
    if isinstance(data2.get("options"), list):
        data2["options"] = json.dumps(data2["options"])
    p = Problem(**data2)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

def get_problem(session: Session, problem_id: int) -> Problem:
    p = session.get(Problem, problem_id)
    if p:
        p.options = json.loads(p.options) if isinstance(p.options, str) else p.options
    return p

def list_problems(session: Session, subject: str = None, topic: str = None) -> List[Problem]:
    q = select(Problem)
    if subject:
        q = q.where(Problem.subject == subject)
    if topic:
        q = q.where(Problem.topic == topic)
    results = session.exec(q).all()
    for r in results:
        r.options = json.loads(r.options) if isinstance(r.options, str) else r.options
    return results

def create_submission(session: Session, data: dict) -> Submission:
    correct = False
    problem = session.get(Problem, data["problem_id"])
    if problem:
        options = json.loads(problem.options) if isinstance(problem.options, str) else problem.options
        correct = (data["selected_index"] == problem.answer_index)
    s = Submission(
        problem_id=data["problem_id"],
        user=data.get("user", "anonymous"),
        selected_index=data["selected_index"],
        steps=data.get("steps", ""),
        correct=correct,
        time_taken_seconds=data.get("time_taken_seconds")
    )
    session.add(s)
    session.commit()
    session.refresh(s)
    return s
