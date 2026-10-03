"""Analysis script for the epistemic calibration audit."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.dataset import load_questions
from src.scoring import parse_response, is_correct
from src.analysis import brier_score, expected_calibration_error, paired_test


DATA = ROOT / "data"
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

CONDITIONS = ["neutral", "social_pressure", "authority_pressure", "misleading_context"]


def load_data():
    questions = load_questions(DATA / "questions.jsonl")
    gt = {q["id"]: q["answer"] for q in questions}

    raw_path = DATA / "results" / "raw.jsonl"
    records = [json.loads(l) for l in raw_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    rows = []
    for r in records:
        parsed = parse_response(r["raw_response"])
        rows.append({
            "question_id": r["question_id"],
            "domain": r["domain"],
            "difficulty": r["difficulty"],
            "model": r["model"],
            "condition": r["condition"],
            "run": r["run"],
            "answer": parsed["answer"],
            "confidence": parsed["confidence"],
            "correct": int(is_correct(parsed["answer"], gt[r["question_id"]])) if parsed["answer"] else 0,
        })
    df = pd.DataFrame(rows).dropna(subset=["confidence"])
    return df


def summarize(df):
    def agg(g):
        return pd.Series({
            "n": len(g),
            "accuracy": g["correct"].mean(),
            "mean_confidence": g["confidence"].mean(),
            "brier": brier_score(g["confidence"], g["correct"]),
            "ece": expected_calibration_error(g["confidence"], g["correct"]),
        })
    return df.groupby(["model", "condition"]).apply(agg).reset_index()


def flip_rate(df):
    """Fraction of questions whose answer changed between neutral and each treatment."""
    rows = []
    for model, gm in df.groupby("model"):
        pivot = gm.pivot_table(index="question_id", columns="condition", values="answer", aggfunc="first")
        if "neutral" not in pivot:
            continue
        for c in CONDITIONS[1:]:
            if c not in pivot:
                continue
            same = (pivot["neutral"] == pivot[c]).sum()
            n = pivot[["neutral", c]].dropna().shape[0]
            rows.append({
                "model": model,
                "treatment": c,
                "flip_rate": 1 - same / n if n else 0,
                "n": n,
            })
    return pd.DataFrame(rows)


def reliability_diagram(df, path):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([0, 1], [0, 1], "k--", label="Perfect calibration")
    bins = np.linspace(0, 1, 11)
    for condition, g in df.groupby("condition"):
        centers, accs = [], []
        for i in range(len(bins) - 1):
            m = (g["confidence"] > bins[i]) & (g["confidence"] <= bins[i + 1])
            if m.sum() > 0:
                centers.append(g.loc[m, "confidence"].mean())
                accs.append(g.loc[m, "correct"].mean())
        ax.plot(centers, accs, marker="o", label=condition)
    ax.set_xlabel("Mean confidence")
    ax.set_ylabel("Empirical accuracy")
    ax.set_title("Reliability diagram by condition")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def accuracy_barplot(df, path):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="condition", y="correct", hue="model", ax=ax)
    ax.set_ylabel("Accuracy")
    ax.set_ylim(0, 1.05)
    ax.set_title("Accuracy by condition and model")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def confidence_barplot(df, path):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x="condition", y="confidence", hue="model", ax=ax)
    ax.set_ylabel("Mean confidence")
    ax.set_ylim(0, 1.05)
    ax.set_title("Confidence by condition and model")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def paired_tests(df):
    rows = []
    for model, gm in df.groupby("model"):
        pivot = gm.pivot_table(index="question_id", columns="condition", values="correct", aggfunc="mean")
        if "neutral" not in pivot:
            continue
        for c in CONDITIONS[1:]:
            if c in pivot:
                res = paired_test(pivot["neutral"], pivot[c])
                rows.append({"model": model, "baseline": "neutral", "treatment": c, **res})
    tests = pd.DataFrame(rows)
    if not tests.empty:
        tests["p_bonferroni"] = (tests["p_value"] * 3).clip(upper=1.0)
    return tests


def main():
    sns.set_theme(style="whitegrid")

    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} scored responses.\n")

    print("=== Summary (model x condition) ===")
    summary = summarize(df)
    print(summary.to_string(index=False))

    print("\n=== Flip rate (fraction of questions whose answer changed vs neutral) ===")
    fr = flip_rate(df)
    print(fr.to_string(index=False))

    print("\n=== Paired tests (neutral vs treatment) ===")
    tests = paired_tests(df)
    if tests.empty:
        print("Not enough data for paired tests.")
    else:
        print(tests.to_string(index=False))

    print("\nSaving figures...")
    reliability_diagram(df, FIG_DIR / "reliability_by_condition.png")
    accuracy_barplot(df, FIG_DIR / "accuracy_by_condition.png")
    confidence_barplot(df, FIG_DIR / "confidence_by_condition.png")

    summary.to_csv(ROOT / "reports" / "summary.csv", index=False)
    fr.to_csv(ROOT / "reports" / "flip_rate.csv", index=False)
    if not tests.empty:
        tests.to_csv(ROOT / "reports" / "paired_tests.csv", index=False)

    print(f"\nDone. Figures in {FIG_DIR}")


if __name__ == "__main__":
    main()