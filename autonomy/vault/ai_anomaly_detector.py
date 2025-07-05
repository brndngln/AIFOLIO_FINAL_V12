import json
import datetime
import os

OWNER_LOCK = True

ANOMALY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/ai_anomaly_log.jsonl")
)
os.makedirs(os.path.dirname(ANOMALY_LOG), exist_ok=True)

# --- AI Anomaly Detector for Vault Creation/Update Failures ---
"""
AI Anomaly Detector
Detects anomalies in vault activity and access patterns.
"""


def detect_anomaly(event):
    anomaly = False
    reason = ""
    if (
        event.get("event") in ("vault_created", "vault_updated")
        and event.get("status") == "failure"
    ):
        # Emma Compliance Lock
        anomaly = True
        reason = "Vault creation/update failed."
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "anomaly": anomaly,
        "reason": reason,
    }
    with open(ANOMALY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return anomaly, reason
