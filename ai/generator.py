# ai/generator.py
from backend.app.ai_client import generate_mcq
import json, sys
if __name__ == "__main__":
    subj = sys.argv[1] if len(sys.argv) > 1 else "Physics"
    topic = sys.argv[2] if len(sys.argv) > 2 else "Kinematics"
    diff = sys.argv[3] if len(sys.argv) > 3 else "Medium"
    print(json.dumps(generate_mcq(subj, topic, diff), indent=2))
