import json
import datetime
import os

ENGAGEMENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'vault_engagement_analytics_log.jsonl'))
os.makedirs(os.path.dirname(ENGAGEMENT_LOG), exist_ok=True)

# --- Vault Engagement Over Time (SAFE AI, Non-Sentient, Owner-Controlled) ---
def log_engagement(vault_id, event_type, user_id=None, metadata=None):
    """
    Logs a vault engagement event in a static, deterministic, SAFE AI-compliant way.
    Returns a dict with result, explanation, recommendation, priority, SAFE AI metadata, and version.
    """
    VERSION = "AIFOLIO_ENGAGEMENT_ENGINE_V2_SAFEAI_FINAL"
    SAFE_AI_COMPLIANT = True
    OWNER_CONTROLLED = True
    NON_SENTIENT = True
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'event_type': event_type,
        'user_id': user_id,
        'metadata': metadata or {}
    }
    with open(ENGAGEMENT_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    explanation = f"Engagement event '{event_type}' logged for vault {vault_id}."
    recommendation = None
    priority = 3
    return {
        'entry': entry,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def calculate_engagement(vault_id, since_days=30):
    """
    Calculates vault engagement count over a static time window.
    Returns a dict with count, explanation, recommendation, priority, SAFE AI metadata, and version.
    """
    VERSION = "AIFOLIO_ENGAGEMENT_ENGINE_V2_SAFEAI_FINAL"
    SAFE_AI_COMPLIANT = True
    OWNER_CONTROLLED = True
    NON_SENTIENT = True
    now = datetime.datetime.utcnow()
    count = 0
    try:
        with open(ENGAGEMENT_LOG, 'r') as f:
            for line in f:
                e = json.loads(line)
                if e['vault_id'] == vault_id:
                    t = datetime.datetime.fromisoformat(e['timestamp'].replace('Z',''))
                    if (now - t).days <= since_days:
                        count += 1
    except FileNotFoundError:
        pass
    explanation = f"Engagement count for vault {vault_id} in last {since_days} days: {count}."
    recommendation = "Increase engagement via targeted campaigns." if count < 5 else None
    priority = 5 if count < 5 else 1
    return {
        'count': count,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

# --- Static Drift/Hallucination Protection (stub) ---
def engagement_drift_protection():
    return {"drift": False, "explanation": "No drift detected."}

# --- Static Feedback Loop (stub, not user learned) ---
def engagement_static_feedback():
    return ["Increase engagement if counts are low."]

# --- Extension Point: Add future static SAFE AI features here ---
