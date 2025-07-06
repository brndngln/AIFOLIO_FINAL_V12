import re
import json
import os
import datetime
from spellchecker import SpellChecker

NORMALIZER_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/ai_output_normalizer_log.jsonl"
    )
)
os.makedirs(os.path.dirname(NORMALIZER_LOG), exist_ok=True)

BRAND_GUIDELINES = [
    "AIFOLIO",
    "reliable",
    "trusted",
    "compliant",
    "ethical",
    "professional",
    "non-sentient",
    "human preview",
]
LEGAL_SAFE_PHRASES = [
    "for informational purposes",
    "not legal advice",
    "compliant with applicable law",
    "no personal data",
]
TONE_WHITELIST = ["professional", "friendly", "neutral", "authoritative"]


# --- Output Normalizer ---
from typing import Any, Dict

def normalize_output(
    text,
    brand_terms=BRAND_GUIDELINES,
    legal_phrases=LEGAL_SAFE_PHRASES,
    tone="professional",
    reading_level=10,
):
    # Check tone
    tone_flag = not any(t in text.lower() for t in TONE_WHITELIST)
    # Check reading level (Flesch-Kincaid grade)
    words = text.split()
    sentences = re.split(r"[.!?]", text)
    syllables = sum(len(re.findall(r"[aeiouy]+", w.lower())) for w in words)
    num_words = len(words)
    num_sentences = max(1, len([s for s in sentences if s.strip()]))
    fk_grade = (
        0.39 * (num_words / num_sentences) + 11.8 * (syllables / num_words) - 15.59
    )
    reading_flag = fk_grade > reading_level
    # Brand guideline check
    brand_flag = not any(b.lower() in text.lower() for b in brand_terms)
    # Legal-safe phrasing check
    legal_flag = not any(l.lower() in text.lower() for l in legal_phrases)
    # Spell check
    spell = SpellChecker()
    spell_flag = list(spell.unknown(words))
    # Compose result
    flags = []
    if tone_flag:
        flags.append("tone")
    if reading_flag:
        flags.append("reading_level")
    if brand_flag:
        flags.append("brand_guidelines")
    if legal_flag:
        flags.append("legal_safe")
    if spell_flag:
        flags.append("spelling")
    result = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "original": text,
        "normalized": text,  # (future: auto-normalize if desired, for now just flag)
        "flags": flags,
        "reading_grade": fk_grade,
        "spelling_errors": spell_flag,
    }
    with open(NORMALIZER_LOG, "a") as f:
        f.write(json.dumps(result) + "\n")
    return result


if __name__ == "__main__":
    # Example usage
    text = "AIFOLIO is a reliable, trusted platform. For informational purposes only."
    out = normalize_output(text)
    print(json.dumps(out, indent=2))
