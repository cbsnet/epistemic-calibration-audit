"""Run the epistemic calibration audit experiment.

Reads questions from data/questions.jsonl, queries each model under each
condition, and writes raw responses to data/results/raw.jsonl.
"""

import json
import sys
import time
from pathlib import Path

# Make `src` importable regardless of the current working directory.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load environment variables from .env (e.g. GROQ_API_KEY).
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from src.dataset import load_questions
from src.runner import run_experiment


if __name__ == "__main__":
    questions_path = ROOT / "data" / "questions.jsonl"
    output_path = ROOT / "data" / "results" / "raw.jsonl"

    questions = load_questions(questions_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loaded {len(questions)} questions from {questions_path}")
    print(f"Writing results to {output_path}")

    run_experiment(questions, output_path)

    print(f"Done. Saved {len(questions)} questions × conditions to {output_path}")
    