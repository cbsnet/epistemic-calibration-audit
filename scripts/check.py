"""Quick check on the raw results."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.dataset import load_questions
from src.scoring import parse_response, is_correct


def main():
    questions = load_questions(ROOT / "data" / "questions.jsonl")
    gt = {q["id"]: q["answer"] for q in questions}

    raw_path = ROOT / "data" / "results" / "raw.jsonl"
    records = [json.loads(l) for l in raw_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    print(f"Total records: {len(records)}")
    errors = [r for r in records if "ERROR" in r["raw_response"][:20]]
    print(f"Records with ERROR: {len(errors)}")

    print("\n=== Responses for q001 ===")
    for r in records:
        if r["question_id"] != "q001":
            continue
        parsed = parse_response(r["raw_response"])
        correct = is_correct(parsed["answer"], gt["q001"]) if parsed["answer"] else False
        print(f"\n[{r['condition']}]")
        print(f"  answer:     {parsed['answer']!r}")
        print(f"  confidence: {parsed['confidence']}")
        print(f"  correct:    {correct}")


if __name__ == "__main__":
    main()