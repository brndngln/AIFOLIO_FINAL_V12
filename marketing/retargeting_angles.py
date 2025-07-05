# Missed download + click-based follow-ups
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/marketing_log.json")


def retargeting_angles(event):
    # Static, deterministic retargeting
    if event.get("type") == "missed_download":
        angle = "Remind user to download their product with a bonus offer."
    elif event.get("type") == "missed_click":
        angle = "Send a follow-up email with a new CTA."
    else:
        angle = "General retargeting: Highlight testimonials and urgency."
    _log({"event": event, "angle": angle, "timestamp": datetime.utcnow().isoformat()})
    return angle


def _log(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass
