import json
from datetime import datetime


def log_engagement(user_id, product_id, action, details):
    log = {
        "user_id": user_id,
        "product_id": product_id,
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "details": details,
    }
    with open("analytics/engagement_log.json", "a") as f:
        f.write(json.dumps(log) + "\n")
