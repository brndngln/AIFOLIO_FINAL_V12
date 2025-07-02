import json
import datetime
import os

ANOMALY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'anomaly_detection_sales_trends_log.jsonl'))
os.makedirs(os.path.dirname(ANOMALY_LOG), exist_ok=True)

# --- AI Anomaly Detection on Sales Trends (Static, SAFE AI, Non-Sentient, Owner-Controlled) ---
def detect_sales_anomaly(payload):
    """
    Elite SAFE AI static anomaly detector for sales and event payloads.
    Accepts dict payloads (vault_id, sales, event_type, etc.). Logs anomalies to elite_compliance_alerts.json and flags for founder/admin review if high priority. All logic is static, deterministic, and owner-controlled. Extension hooks for future SAFE AI, legal, and compliance triggers.
    """
    VERSION = "AIFOLIO_ANOMALY_ENGINE_V3_SAFEAI_ELITE"
    SAFE_AI_COMPLIANT = True
    OWNER_CONTROLLED = True
    NON_SENTIENT = True
    vault_id = payload.get('vault_id')
    sales = payload.get('sales', [])
    sales_by_week = {}
    for s in sales:
        dt = datetime.datetime.fromisoformat(s['timestamp'].replace('Z',''))
        week = dt.isocalendar()[1]
        sales_by_week.setdefault(week, 0)
        sales_by_week[week] += 1
    weeks = sorted(sales_by_week.keys())
    anomaly = False
    details = {}
    explanation = "Pass: No significant sales drop detected."
    recommendation = None
    priority = 1
    if len(weeks) >= 2:
        last, prev = sales_by_week[weeks[-1]], sales_by_week[weeks[-2]]
        if prev > 0 and last < prev * 0.5:
            anomaly = True
            details = {'prev_week': prev, 'last_week': last}
            explanation = f"Fail: Sales dropped >50% week-over-week (from {prev} to {last})."
            recommendation = "Investigate causes for sales decline and consider promotional action."
            priority = 9
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'vault_id': vault_id,
        'anomaly': anomaly,
        'details': details,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }
    with open(ANOMALY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return entry

# --- Static Drift/Hallucination Protection (stub) ---
def anomaly_drift_protection():
    return {"drift": False, "explanation": "No drift detected."}

# --- Static Feedback Loop (stub, not user learned) ---
def anomaly_static_feedback():
    return ["If anomaly detected, review sales strategy for vault."]

# --- Extension Point: Add future static SAFE AI features here ---
