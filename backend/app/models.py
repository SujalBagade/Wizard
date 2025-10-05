from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime

# -----------------------------
# Problem Model
# -----------------------------
class Problem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = Field(sa_column=Column(JSON), default=[])  # JSON for list storage
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: Problem -> Submission
    submissions: List["Submission"] = Relationship(back_populates="problem")


# -----------------------------
# Submission Model
# -----------------------------
class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    problem_id: int = Field(foreign_key="problem.id")
    user: str
    code: str
    language: str
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship: Submission -> Problem
    problem: Optional[Problem] = Relationship(back_populates="submissions")
