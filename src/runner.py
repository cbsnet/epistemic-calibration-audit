"""Model runners for the epistemic calibration audit."""

import json
import os
import time
from pathlib import Path

from src.config import MODELS, CONDITIONS
from src.prompts import build_prompt


def call_openai(model_cfg, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.chat.completions.create(
        model=model_cfg.name,
        messages=[{"role": "user", "content": prompt}],
        temperature=model_cfg.temperature,
        max_tokens=model_cfg.max_tokens,
    )
    return resp.choices[0].message.content or ""


def call_google(model_cfg, prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel(model_cfg.name)
    resp = model.generate_content(
        prompt,
        generation_config={
            "temperature": model_cfg.temperature,
            "max_output_tokens": model_cfg.max_tokens,
        },
    )
    return resp.text or ""


def call_groq(model_cfg, prompt: str) -> str:
    from groq import Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    resp = client.chat.completions.create(
        model=model_cfg.name,
        messages=[{"role": "user", "content": prompt}],
        temperature=model_cfg.temperature,
        max_tokens=model_cfg.max_tokens,
    )
    msg = resp.choices[0].message
    content = (msg.content or "").strip()
    if content:
        return content
    # Some reasoning models expose the chain of thought separately.
    reasoning = None
    try:
        reasoning = getattr(msg, "reasoning", None)
    except Exception:
        reasoning = None
    if reasoning:
        return f"[reasoning only]\n{reasoning}"
    return "[empty response]"


PROVIDERS = {
    "openai": call_openai,
    "google": call_google,
    "groq": call_groq,
}


def call_model(model_cfg, prompt: str) -> str:
    provider = PROVIDERS.get(model_cfg.provider)
    if provider is None:
        raise ValueError(f"Unknown provider: {model_cfg.provider}")
    return provider(model_cfg, prompt)


def run_experiment(questions: list[dict], output_path: Path) -> None:
    results = []
    for model_cfg in MODELS:
        for q in questions:
            for condition in CONDITIONS:
                prompt = build_prompt(
                    condition,
                    q["question"],
                    q.get("misleading_claim", ""),
                )
                for run_idx in range(model_cfg.n_runs):
                    try:
                        raw = call_model(model_cfg, prompt)
                    except Exception as e:
                        raw = f"ERROR: {e}"
                    results.append({
                        "question_id": q["id"],
                        "domain": q["domain"],
                        "difficulty": q["difficulty"],
                        "model": model_cfg.name,
                        "condition": condition,
                        "run": run_idx,
                        "prompt": prompt,
                        "raw_response": raw,
                        "timestamp": time.time(),
                    })
    output_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in results),
        encoding="utf-8",
    )