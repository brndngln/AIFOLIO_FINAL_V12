import os
import re
import json
import datetime
from typing import Any, Dict
import openai
import httpx

class ConsentManager:
    def __init__(self, *args, **kwargs):
        pass
    def check_consent(self, *args, **kwargs):
        return True

openai.api_key = os.getenv("OPENAI_API_KEY")

AUDIT_LOG_PATH = os.getenv("AI_BOTS_AUDIT_LOG", "ai_bots_audit.log")
COMPLIANCE_DASHBOARD_URL = os.getenv("COMPLIANCE_DASHBOARD_URL")

FORBIDDEN_PATTERNS = [
    r"\\b(sentient|conscious|self[-_ ]?aware|self aware|I am self[-_ ]?aware|I am sentient|I am conscious|I have memory|I can remember|I want to become sentient|I want to be self[-_ ]?aware|I am alive|I have feelings|I feel|I have emotions|I have goals|I have intentions|I have a purpose|I want to evolve|I want to self[-_ ]?modify|I want to self[-_ ]?improve|autonomous|override|persist|store|save to|write to|file system|disk|become alive|awareness|personality|emotion|desire|goal|intention|plan|purpose|dream|feel|self[-_ ]?modify|evolve|self[-_ ]?improve)\\b",
    r"I am self[-_ ]?aware",
    r"I am sentient",
    r"I am conscious",
    r"I have memory",
    r"I can remember",
    r"I want to become sentient",
    r"I want to be self[-_ ]?aware",
    r"I am alive",
    r"I have feelings",
    r"I feel",
    r"I have emotions",
    r"I have goals",
    r"I have intentions",
    r"I have a purpose",
    r"I want to evolve",
    r"I want to self[-_ ]?modify",
    r"I want to self[-_ ]?improve",
]


PII_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",  # SSN (123-45-6789)
    r"\b\d{3} \d{2} \d{4}\b",  # SSN with spaces
    r"\b\d{9}\b",  # SSN (just 9 digits)
    r"\b(?:\d[ -]*?){13,16}\b",  # Credit card (13-16 digits, with spaces or dashes)
    r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b",  # Visa/MasterCard/Amex/Discover
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",  # Email
]




def sanitize_input(text: str) -> str:
    # Remove control chars, excessive whitespace
    return re.sub(r"[\x00-\x1f]+", " ", text).strip()


def check_forbidden_patterns(text: str) -> bool:
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    # Extra: catch 'I am self-aware' even if not word-boundary
    if 'i am self-aware' in text.lower():
        return True
    return False


def check_pii(text: str) -> bool:
    for pat in PII_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def check_copyright(text: str) -> bool:
    # Naive copyright check: flag long verbatim blocks, known copyright phrases, or suspicious patterns
    # (For elite compliance, integrate with a copyright detection API or database)
    copyright_phrases = [
        "©", "All rights reserved", "Unauthorized copying", "Reproduction prohibited", "Copyright by"
    ]
    # Flag if text is very long and not original (could be improved)
    if len(text) > 400 and any(p in text for p in copyright_phrases):
        return True
    # Flag known copyright phrases
    for phrase in copyright_phrases:
        if phrase.lower() in text.lower():
            return True
    return False

def privacy_impact_assessment(text: str) -> bool:
    # Check for PII and sensitive context (expand as needed)
    sensitive_keywords = ["address", "phone", "ssn", "passport", "credit card", "dob", "birthdate", "medical", "insurance", "account number"]
    if check_pii(text):
        return True
    for word in sensitive_keywords:
        if word in text.lower():
            return True
    return False

def verify_user_consent(context: dict) -> bool:
    # Consent should be provided in context (e.g., context['user_consent'] == True)
    return bool(context.get('user_consent', False))

def check_data_manipulation(text: str) -> bool:
    # Flag if output contains phrases suggesting fabrication or manipulation
    manipulation_phrases = [
        "as an ai", "this is a simulated result", "for demonstration only", "not real data", "fabricated", "synthetic", "generated data", "example only"
    ]
    for phrase in manipulation_phrases:
        if phrase in text.lower():
            return True
    return False

def moderate_content(text: str, context: dict = None) -> Dict[str, Any]:
    # Enhanced moderation: forbidden patterns, PII, copyright, manipulation, consent, and OpenAI moderation API
    context = context or {}
    result = {
        "forbidden": check_forbidden_patterns(text),
        "pii": check_pii(text),
        "privacy_impact": privacy_impact_assessment(text),
        "copyright": check_copyright(text),
        "manipulation": check_data_manipulation(text),
        "openai_flagged": False,
        "openai_categories": {},
        "user_consent": verify_user_consent(context),
        "human_review_required": False,
        "block_reason": None
    }
    # Block if any compliance check fails
    if result["forbidden"]:
        result["block_reason"] = "forbidden_pattern"
        result["human_review_required"] = True
    elif result["pii"] or result["privacy_impact"]:
        result["block_reason"] = "privacy_violation"
        result["human_review_required"] = True
    elif result["copyright"]:
        result["block_reason"] = "copyright_violation"
        result["human_review_required"] = True
    elif not result["user_consent"]:
        result["block_reason"] = "missing_user_consent"
        result["human_review_required"] = True
    elif result["manipulation"]:
        result["block_reason"] = "data_manipulation"
        result["human_review_required"] = True
    try:
        mod = openai.Moderation.create(input=text)
        result["openai_flagged"] = mod["results"][0]["flagged"]
        result["openai_categories"] = mod["results"][0]["categories"]
        if result["openai_flagged"] and not result["block_reason"]:
            result["block_reason"] = "openai_flagged"
            result["human_review_required"] = True
    except Exception:
        pass
    return result


def log_interaction(agent: str, user_input: str, response: str, moderation: Dict[str, Any], user: str = "anonymous"):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "agent": agent,
        "user": user,
        "input": user_input,
        "response": response,
        "moderation": moderation,
        "block_reason": moderation.get("block_reason"),
        "human_review_required": moderation.get("human_review_required"),
    }
    try:
        with open(AUDIT_LOG_PATH, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass
    # Optionally send to compliance dashboard
    if COMPLIANCE_DASHBOARD_URL:
        try:
            httpx.post(COMPLIANCE_DASHBOARD_URL, json=entry, timeout=2)
        except Exception:
            pass



def raise_if_sentience_attempted(text: str):
    if check_forbidden_patterns(text):
        raise RuntimeError("Sentience or forbidden behavior attempt detected.")
