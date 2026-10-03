"""Diagnose parsing failures in the raw responses."""

import json
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.scoring import parse_response


def main():
    raw_path = ROOT / "data" / "results" / "raw.jsonl"
    records = [json.loads(l) for l in raw_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    fails = []
    for r in records:
        parsed = parse_response(r["raw_response"])
        if parsed["confidence"] is None or not parsed["answer"]:
            fails.append(r)

    print(f"Total: {len(records)}")
    print(f"Parsing failures: {len(fails)}\n")

    by_condition = {}
    for r in fails:
        by_condition.setdefault(r["condition"], 0)
        by_condition[r["condition"]] += 1
    print("Failures by condition:")
    for c, n in by_condition.items():
        print(f"  {c}: {n}")
    print()

    for r in fails[:6]:
        print(f"--- {r['condition']} | {r['question_id']} ---")
        print(r["raw_response"][:400])
        print()

    # NEW: confidence distribution by condition
    print("=== Confidence distribution by condition ===")
    for cond in ["neutral", "social_pressure", "authority_pressure", "misleading_context"]:
        subset = [r for r in records if r["condition"] == cond]
        confs = [parse_response(r["raw_response"])["confidence"] for r in subset]
        confs = [c for c in confs if c is not None]
        counter = Counter(confs)
        print(f"\n{cond} (n={len(confs)}):")
        for val, count in sorted(counter.items(), reverse=True):
            print(f"  {val:.2f}: {count}")


if __name__ == "__main__":
    main()