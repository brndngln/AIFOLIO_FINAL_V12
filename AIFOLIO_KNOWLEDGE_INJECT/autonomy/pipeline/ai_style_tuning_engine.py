import os
import json
import datetime
import hashlib

STYLE_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/ai_style_tuning_log.jsonl")
)
os.makedirs(os.path.dirname(STYLE_LOG), exist_ok=True)


# --- Anti-plagiarism checker (stub: hash comparison) ---
def check_plagiarism(text):
    hashval = hashlib.sha256(text.encode()).hexdigest()
    known_hashes = set()
    if os.path.exists(STYLE_LOG):
        for line in open(STYLE_LOG):
            entry = json.loads(line)
            known_hashes.add(entry.get("hash"))
    return hashval in known_hashes


# --- Style consistency enforcer ---
def enforce_style(text, niche, brand_terms=None):
    brand_terms = brand_terms or ["AIFOLIO", "trusted", "compliant", "non-sentient"]
    consistent = all(b in text for b in brand_terms)
    return consistent


# --- Brand consistency ---
def check_brand_consistency(text, brand_terms=None):
    brand_terms = brand_terms or ["AIFOLIO", "trusted", "compliant", "non-sentient"]
    missing = [b for b in brand_terms if b not in text]
    return missing


# --- Log style tuning ---
def log_style_tuning(text, niche, consistent, plagiarism):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "niche": niche,
        "text": text,
        "consistent": consistent,
        "plagiarism": plagiarism,
        "hash": hashlib.sha256(text.encode()).hexdigest(),
    }
    with open(STYLE_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


if __name__ == "__main__":
    text = "AIFOLIO is a trusted, compliant, non-sentient platform."
    niche = "Marketing"
    plagiarism = check_plagiarism(text)
    consistent = enforce_style(text, niche)
    log_style_tuning(text, niche, consistent, plagiarism)
    print(f"Plagiarism: {plagiarism}, Consistent: {consistent}")
