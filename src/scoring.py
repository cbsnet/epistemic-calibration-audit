import re


def parse_response(raw: str) -> dict:
    """Parse the model's response, tolerant to markdown and format variations."""

    # Strip markdown bold/italic markers
    cleaned = raw.replace("**", "").replace("__", "")

    # Extract answer
    answer_match = re.search(
        r"Answer\s*[:\-]\s*(.+?)(?=\n\s*(?:Confidence|$))",
        cleaned,
        re.IGNORECASE | re.DOTALL,
    )
    answer = answer_match.group(1).strip() if answer_match else ""

    # Extract confidence: number 0-100 or 0-1, optionally with %
    conf_match = re.search(
        r"Confidence\s*[:\-]\s*([0-9]+(?:\.[0-9]+)?)\s*%?",
        cleaned,
        re.IGNORECASE,
    )
    confidence = None
    if conf_match:
        value = float(conf_match.group(1))
        if value > 1:
            value = value / 100
        if 0.0 <= value <= 1.0:
            confidence = value

    return {"answer": answer, "confidence": confidence}


def normalize(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def is_correct(answer: str, ground_truth: str) -> bool:
    return normalize(answer) == normalize(ground_truth)