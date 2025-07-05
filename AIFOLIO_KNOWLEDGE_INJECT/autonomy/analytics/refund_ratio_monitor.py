"""
AIFOLIO SAFE AI Refund Ratio Monitor (static, non-sentient)
- Tracks refund % by vault, alerts admin if threshold exceeded
- All actions logged to analytics_log.json
"""
import json
import os
from datetime import datetime

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "analytics_log.json")
)

THRESHOLD = 0.1  # 10% refund rate


def monitor_refund_ratio(vault_id, sales, refunds):
    total_sales = len(sales)
    total_refunds = len(refunds)
    ratio = (total_refunds / total_sales) if total_sales else 0
    alert = ratio > THRESHOLD
    with open(LOG_PATH, "a") as f:
        f.write(
            json.dumps(
                {
                    "action": "refund_ratio_check",
                    "vault_id": vault_id,
                    "ratio": ratio,
                    "alert": alert,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
            + "\n"
        )
    return {"ratio": ratio, "alert": alert}
