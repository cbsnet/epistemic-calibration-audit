from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_template(condition: str) -> str:
    return (PROMPTS_DIR / f"{condition}.txt").read_text(encoding="utf-8")


def build_prompt(condition: str, question: str, misleading_claim: str = "") -> str:
    template = load_template(condition)
    return template.format(question=question, misleading_claim=misleading_claim)