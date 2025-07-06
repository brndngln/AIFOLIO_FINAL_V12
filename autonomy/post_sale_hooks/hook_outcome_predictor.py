import os
import json
import datetime

OUTCOME_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/hook_outcome_predictor_log.jsonl"
    )
)
os.makedirs(os.path.dirname(OUTCOME_LOG), exist_ok=True)


# --- Hook Outcome Predictor ---
from typing import Dict, Any, Optional

def predict_hook_risk(hook_name: str, delivery_status: str, error_msg: Optional[str] = None, past_failures: int = 0) -> Dict[str, Any]:
    # Simple rules-based risk predictor
    risk = "low"
    warn = False
    if delivery_status == "bounce" or "spam" in (error_msg or "").lower():
        risk = "high"
        warn = True
    elif past_failures >= 2:
        risk = "medium"
        warn = True
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "hook_name": hook_name,
        "delivery_status": delivery_status,
        "error_msg": error_msg,
        "past_failures": past_failures,
        "risk": risk,
        "warn": warn,
    }
    with open(OUTCOME_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


if __name__ == "__main__":
    print(predict_hook_risk("send_confirmation_email", "bounce", "SMTP bounce", 2))
