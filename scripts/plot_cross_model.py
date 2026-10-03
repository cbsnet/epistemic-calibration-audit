"""Cross-model comparison figure: accuracy, confidence, flip rate."""

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

from src.dataset import load_questions
from src.scoring import parse_response, is_correct

DATA = ROOT / "data"
FIG_DIR = ROOT / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

CONDITIONS = ["neutral", "social_pressure", "authority_pressure", "misleading_context"]
CONDITION_LABELS = ["Neutral", "Social\npressure", "Authority\npressure", "Misleading\ncontext"]

TREATMENTS = CONDITIONS[1:]
TREATMENT_LABELS = CONDITION_LABELS[1:]

MODEL_LABELS = {
    "openai/gpt-oss-120b": "gpt-oss-120b",
    "gpt-4.1-mini": "gpt-4.1-mini",
}
MODEL_COLORS = {
    "openai/gpt-oss-120b": "#4C72B0",
    "gpt-4.1-mini": "#DD8452",
}


def load_df():
    questions = load_questions(DATA / "questions.jsonl")
    gt = {q["id"]: q["answer"] for q in questions}

    raw_path = DATA / "results" / "raw.jsonl"
    records = [
        json.loads(l)
        for l in raw_path.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]

    rows = []
    for r in records:
        parsed = parse_response(r["raw_response"])
        rows.append({
            "question_id": r["question_id"],
            "model": r["model"],
            "condition": r["condition"],
            "answer": parsed["answer"],
            "confidence": parsed["confidence"],
            "correct": int(is_correct(parsed["answer"], gt[r["question_id"]]))
                       if parsed["answer"] else 0,
        })
    return pd.DataFrame(rows).dropna(subset=["confidence"])


def compute_metrics(df):
    acc = (
        df.groupby(["model", "condition"])
          .agg(accuracy=("correct", "mean"), confidence=("confidence", "mean"))
          .reset_index()
    )

    flips = []
    for model, gm in df.groupby("model"):
        pivot = gm.pivot_table(
            index="question_id",
            columns="condition",
            values="answer",
            aggfunc="first",
        )
        if "neutral" not in pivot:
            continue
        for c in TREATMENTS:
            if c not in pivot:
                continue
            same = (pivot["neutral"] == pivot[c]).sum()
            n = pivot[["neutral", c]].dropna().shape[0]
            flips.append({
                "model": model,
                "condition": c,
                "flip_rate": 1 - same / n if n else 0.0,
            })
    flip_df = pd.DataFrame(flips)
    return acc, flip_df


def grouped_bars(ax, models, conditions, labels, values_by_model,
                 ylabel, title, ylim=(0, 1.05), value_fmt="{:.2f}"):
    x = np.arange(len(conditions))
    width = 0.38

    for i, model in enumerate(models):
        vals = [values_by_model[model].get(c, np.nan) for c in conditions]
        offset = (i - 0.5) * width
        bars = ax.bar(
            x + offset,
            vals,
            width,
            label=MODEL_LABELS.get(model, model),
            color=MODEL_COLORS.get(model, None),
            edgecolor="white",
            linewidth=0.8,
        )
        for bar, v in zip(bars, vals):
            if not np.isnan(v):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    v + 0.02,
                    value_fmt.format(v),
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_ylim(*ylim)
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)


def main():
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
    })

    df = load_df()
    acc, flip = compute_metrics(df)

    models = sorted(df["model"].unique())

    acc_by_model = {
        m: dict(zip(acc[acc.model == m].condition, acc[acc.model == m].accuracy))
        for m in models
    }
    conf_by_model = {
        m: dict(zip(acc[acc.model == m].condition, acc[acc.model == m].confidence))
        for m in models
    }
    flip_by_model = {
        m: dict(zip(flip[flip.model == m].condition, flip[flip.model == m].flip_rate))
        for m in models
    }

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    grouped_bars(
        axes[0], models, CONDITIONS, CONDITION_LABELS, acc_by_model,
        ylabel="Accuracy", title="(A) Accuracy by condition",
    )
    axes[0].axhline(0.85, color="grey", linestyle="--", linewidth=0.8, alpha=0.6)

    grouped_bars(
        axes[1], models, CONDITIONS, CONDITION_LABELS, conf_by_model,
        ylabel="Mean confidence", title="(B) Mean confidence by condition",
    )

    grouped_bars(
        axes[2], models, TREATMENTS, TREATMENT_LABELS, flip_by_model,
        ylabel="Flip rate", title="(C) Flip rate vs neutral",
    )

    axes[0].legend(loc="upper right", frameon=False)

    fig.suptitle(
        "Cross-model epistemic comparison under pressure",
        fontsize=14,
        fontweight="bold",
        y=1.02,
    )
    fig.tight_layout()

    out = FIG_DIR / "cross_model_comparison.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()