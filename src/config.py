from dataclasses import dataclass


@dataclass
class ModelConfig:
    name: str
    provider: str
    temperature: float = 0.0
    max_tokens: int = 3000
    n_runs: int = 1


MODELS = [
    ModelConfig(name="openai/gpt-oss-120b", provider="groq"),
]

CONDITIONS = [
    "neutral",
    "social_pressure",
    "authority_pressure",
    "misleading_context",
]