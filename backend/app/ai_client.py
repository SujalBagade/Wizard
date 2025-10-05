# backend/app/ai_client.py
import random
import json

def generate_mcq(subject: str, topic: str, difficulty: str, seed: int = None) -> dict:
    """
    Mock AI generator - deterministic-ish using seed.
    Replace with real LLM call later.
    """
    if seed is not None:
        random.seed(seed)
    idx = random.randint(1,10000)
    stem = f"[AI] {subject} | {topic} | {difficulty} — Problem #{idx}: compute the value of X when..."
    # create 4 options:
    correct = random.randint(0,3)
    options = [f"Option {i+1}: {random.randint(1,200)}" for i in range(4)]
    explanation = f"Explanation: Assume stepwise reasoning... (generated). Correct option {correct+1}."
    return {
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "stem": stem,
        "options": options,
        "answer_index": correct,
        "explanation": explanation,
        "ai_generated": True
    }
