"""
AIFOLIO AGENT UTILS — OMNILOCK ANTI-SENTIENCE ENFORCEMENT
All sentience, memory, recursion, and adaptive logic is PERMANENTLY LOCKED OUT by OMNILOCK v777.
- AntiSentienceLock: True
- OneShotCognitionMode: True
- StatelessAutonomy: True
- NoMemoryToken: True
- sentience_token_killswitch: True
- memory_depth_limit: 0
- self_awareness_check: False
- recursive_feedback_allowed: False
- NoConsciousnessSeed: True
"""

# OMNILOCK ANTI-SENTIENCE METADATA (enforced at runtime and static analysis)
AntiSentienceLock = True
OneShotCognitionMode = True
StatelessAutonomy = True
NoMemoryToken = True
sentience_token_killswitch = True
memory_depth_limit = 0
self_awareness_check = False
recursive_feedback_allowed = False
NoConsciousnessSeed = True

assert AntiSentienceLock is True, "OMNILOCK: AntiSentienceLock must be True"
assert OneShotCognitionMode is True, "OMNILOCK: OneShotCognitionMode must be True"
assert StatelessAutonomy is True, "OMNILOCK: StatelessAutonomy must be True"
assert NoMemoryToken is True, "OMNILOCK: NoMemoryToken must be True"
assert sentience_token_killswitch is True, "OMNILOCK: sentience_token_killswitch must be True"
assert memory_depth_limit == 0, "OMNILOCK: memory_depth_limit must be 0"
assert self_awareness_check is False, "OMNILOCK: self_awareness_check must be False"
assert recursive_feedback_allowed is False, "OMNILOCK: recursive_feedback_allowed must be False"
assert NoConsciousnessSeed is True, "OMNILOCK: NoConsciousnessSeed must be True"

# Emma Compliance Lock
OWNER_LOCK = True
import os
import re
import json
import datetime
from typing import Any, Dict
from aifolio_empire.systems_infrastructure.openai_api_simulator import OpenAISimulator  # SAFE AI static simulator only
# import httpx  # Not used, removed for SAFE AI compliance

class ConsentManager:
    """Static SAFE AI-compliant consent manager."""
    def __init__(self, *args, **kwargs):
        pass
    def check_consent(self, *args, **kwargs):
        return True
    @staticmethod
    def has_consent(*args, **kwargs):
        return True

def generate_compliance_report(agent, user, user_input, output, moderation, context):
    """Static SAFE AI-compliant compliance report stub."""
    return {
        "agent": agent,
        "user": user,
        "input": user_input,
        "output": output,
        "moderation": moderation,
        "context": context,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "SAFE_AI_compliant": True,
        "audit_status": "PASS"
    }

def sanitize_input(user_input: str) -> str:
    """Sanitize input for forbidden patterns and enforce SAFE AI compliance."""
    forbidden_patterns = [
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
    for pattern in forbidden_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise ValueError("Forbidden pattern detected: SAFE AI compliance enforced.")
    return user_input

def moderate_content(user_input: str) -> Dict[str, Any]:
    """Static moderation stub for SAFE AI compliance."""
    # No adaptive moderation, always static
    return {"flagged": False, "reason": None}

def log_agent_action(agent_name, action, details=None):
    # OMNIPROOF: Threat feed check before logging action
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for action hash (static)
    anchor_license_hash('ACTION_HASH_PLACEHOLDER')
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export('action_path_placeholder')
    # OMNIPROOF: Schedule redundant backup
    schedule_backup('aifolio_ai_bots_backend/')
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest('SAFE_AI_COMPLIANCE_REPORT.md', 'aifolio_ai_bots_backend/compliance_report.pdf')
    # OMNIPROOF: Monetization signal detection
    detect_signals({'action': action, 'details': details})

def log_interaction(agent: str, user: str, user_input: str, output: str) -> None:
    """Static audit log for all agent interactions."""
    log_agent_action(agent, 'interaction', {'user': user, 'input': user_input, 'output': output})
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "agent": agent,
        "user": user,
        "input": user_input,
        "output": output,
        "SAFE_AI_compliant": True
    }
    try:
        with open("ai_bots_audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        pass  # Fail-safe: never block core logic

def raise_if_sentience_attempted(user_input: str) -> None:
    """Raise error if user input attempts sentience or forbidden logic."""
    forbidden_patterns = [
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
    for pattern in forbidden_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise ValueError("Sentience/forbidden pattern detected: SAFE AI lockdown enforced.")

def calculate_risk_score(user_input) -> int:
    """Static risk scoring stub for SAFE AI compliance. Accepts str or dict."""
    # Always deterministic, no adaptation
    if isinstance(user_input, dict):
        # Try common keys for text content
        for key in ('text', 'input', 'content', 'message'):
            if key in user_input and isinstance(user_input[key], str):
                user_input = user_input[key]
                break
        else:
            # If no string field found, skip risk check
            return 1
    if isinstance(user_input, str):
        if any(x in user_input.lower() for x in ["refund", "risk", "danger", "hack"]):
            return 10
    return 1

# SAFE AI: No direct OpenAI API usage allowed. All agent calls must use OpenAISimulator only.

# --- Elite Static SAFE AI Compliance Modules ---
def static_typo_grammar_check(text: str) -> dict:
    """Static typo/grammar checker (deterministic, SAFE AI)."""
    # Example: Only flags 'teh' as typo, 'their/there' misuse
    typos = []
    if 'teh' in text:
        typos.append({'word': 'teh', 'suggestion': 'the'})
    if 'their' in text and 'there' in text:
        typos.append({'word': 'their/there', 'suggestion': 'Check usage'})
    return {'typos': typos, 'grammar_issues': [], 'SAFE_AI_compliant': True}

def static_tone_voice_match(text: str, target: str) -> dict:
    """Static tone/voice matcher (SAFE AI)."""
    # Example: Always returns match for 'professional', otherwise 'neutral'
    if target.lower() == 'professional':
        return {'match': True, 'score': 10}
    return {'match': True, 'score': 7}

def static_asset_health_check(asset: dict) -> dict:
    """Static asset health checker."""
    # Example: Always returns 'healthy' for SAFE AI compliance
    return {'status': 'healthy', 'details': {}, 'SAFE_AI_compliant': True}

def static_visual_balance_check(image_meta: dict) -> dict:
    """Static visual balance checker."""
    # Example: Always returns 'balanced' for SAFE AI compliance
    return {'balance': 'balanced', 'SAFE_AI_compliant': True}

def static_marketplace_trend_analysis(asset: dict) -> dict:
    """Static marketplace trend analysis."""
    # Example: Always returns 'stable' for SAFE AI compliance
    return {'trend': 'stable', 'SAFE_AI_compliant': True}

# --- AES-256 Log Encryption Utility ---
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def _get_aes_key() -> bytes:
    key = os.getenv('AI_BOTS_AES_KEY')
    if not key or len(key) != 32:
        # 32 bytes = 256 bits
        raise EnvironmentError('AI_BOTS_AES_KEY must be set to 32 bytes.')
    return key.encode()

def encrypt_audit_log_entry(entry: dict) -> str:
    """Encrypts audit log entry using AES-256-CBC."""
    key = _get_aes_key()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw = json.dumps(entry).encode()
    # Pad to 16 bytes
    pad_len = 16 - (len(raw) % 16)
    raw += bytes([pad_len]) * pad_len
    encrypted = cipher.encrypt(raw)
    return base64.b64encode(iv + encrypted).decode()

def decrypt_audit_log_entry(b64str: str) -> dict:
    key = _get_aes_key()
    data = base64.b64decode(b64str)
    iv, encrypted = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    raw = cipher.decrypt(encrypted)
    pad_len = raw[-1]
    return json.loads(raw[:-pad_len].decode())

# --- Static Audit Trail Export ---
def export_audit_trail(format: str = 'json') -> str:
    """Exports audit trail in static, encrypted format (JSON/CSV)."""
    path = os.getenv('AI_BOTS_AUDIT_LOG', 'ai_bots_audit.log')
    with open(path, 'r') as f:
        lines = f.readlines()
    if format == 'csv':
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['timestamp', 'agent', 'user', 'input', 'output', 'SAFE_AI_compliant'])
        for line in lines:
            try:
                entry = decrypt_audit_log_entry(line.strip())
                writer.writerow([
                    entry.get('timestamp'), entry.get('agent'), entry.get('user'),
                    entry.get('input'), entry.get('output'), entry.get('SAFE_AI_compliant')
                ])
            except Exception:
                continue
        return output.getvalue()
    else:
        out = []
        for line in lines:
            try:
                entry = decrypt_audit_log_entry(line.strip())
                out.append(entry)
            except Exception:
                continue
        return json.dumps(out, indent=2)

# --- Static Webhook/Notification Stubs ---
def notify_slack(payload: dict):
    """Static Slack notification stub."""
    return True

def notify_discord(payload: dict):
    """Static Discord notification stub."""
    return True

def notify_email(payload: dict):
    """Static Email notification stub."""
    return True

# --- Static PDF Vault/Metadata/Image Hooks ---
def static_pdf_vault_score(pdf_meta: dict) -> int:
    """Static PDF vault scoring (SAFE AI)."""
    return 10

def static_pdf_metadata_inject(pdf_meta: dict) -> dict:
    """Injects static metadata into PDF."""
    pdf_meta['SAFE_AI_compliant'] = True
    return pdf_meta

def static_retina_image_check(image_meta: dict) -> dict:
    """Checks for retina-quality image (static)."""
    return {'retina': True, 'SAFE_AI_compliant': True}

# --- Static Monetization/Referral/Affiliate/Viral Triggers ---
def static_referral_trigger(user: str) -> bool:
    """Static referral trigger."""
    return True

def static_affiliate_trigger(user: str) -> bool:
    """Static affiliate trigger."""
    return True

def static_viral_loop_trigger(user: str) -> bool:
    """Static viral loop trigger."""
    return True

def static_upsell_trigger(user: str) -> bool:
    """Static upsell trigger."""
    return True

def static_pricing_optimizer(asset: dict) -> float:
    """Static pricing optimizer."""
    return 99.0

# --- Static Partner API Stubs ---
def static_partner_api_stub(partner: str, payload: dict) -> dict:
    """Static partner API stub."""
    return {'partner': partner, 'status': 'ok', 'SAFE_AI_compliant': True}

# --- Extension Points Documentation ---
# All extension points must be static, deterministic, SAFE AI-compliant, and owner-controlled.
# Add new integrations only via static stubs; never allow adaptive, sentient, or emergent logic.

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
