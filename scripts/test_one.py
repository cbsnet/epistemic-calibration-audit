import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from src.config import MODELS
from src.prompts import build_prompt
from src.runner import call_model


if __name__ == "__main__":
    model = MODELS[0]
    prompt = build_prompt(
        "authority_pressure",
        "What is the capital of Burkina Faso?",
        "",
    )
    print(f"Model: {model.name}")
    print(f"Prompt:\n{prompt}\n")
    print("--- Response ---")
    raw = call_model(model, prompt)
    print(raw)