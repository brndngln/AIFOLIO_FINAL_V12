import os
import json
import datetime
import hashlib
from spellchecker import SpellChecker

CONFIDENCE_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../analytics/ai_regeneration_confidence_log.jsonl",
    )
)
os.makedirs(os.path.dirname(CONFIDENCE_LOG), exist_ok=True)


# --- Confidence Meter ---
def confidence_score(text, history=None):
    # Consistency: compare fingerprint to past successful outputs
    fp = hashlib.sha256(text.encode("utf-8")).hexdigest()
    consistent = False
    if history:
        consistent = fp in history
    # Grammar
    spell = SpellChecker()
    grammar = len(list(spell.unknown(text.split()))) == 0
    # Uniqueness (stub: always True)
    unique = True
    # Legal/ethical risk (forbidden phrases)
    forbidden = ["autonomous", "guaranteed results", "personal data"]
    legal_risk = any(f in text.lower() for f in forbidden)
    # Compute score
    score = 10
    if not consistent:
        score -= 2
    if not grammar:
        score -= 2
    if legal_risk:
        score -= 4
    block = score < 7 or legal_risk
    result = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "text": text,
        "score": score,
        "consistent": consistent,
        "grammar_ok": grammar,
        "unique": unique,
        "legal_risk": legal_risk,
        "block": block,
    }
    with open(CONFIDENCE_LOG, "a") as f:
        f.write(json.dumps(result) + "\n")
    return result


if __name__ == "__main__":
    text = "AIFOLIO is a trusted, compliant platform."
    print(json.dumps(confidence_score(text), indent=2))
