import os
import json
from datetime import datetime

REQUESTS_PATH = os.path.join(os.path.dirname(__file__), "gdpr_deletion_requests.json")


def submit_gdpr_deletion_request(user_id: str, email: str, reason: str = "") -> str:
    """
    Log a GDPR deletion request for a user.
    """
    if os.path.exists(REQUESTS_PATH):
        with open(REQUESTS_PATH, "r") as f:
            data = json.load(f)
    else:
        data = {"requests": []}
    req = {
        "user_id": user_id,
        "email": email,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
    }
    data["requests"].append(req)
    with open(REQUESTS_PATH, "w") as f:
        json.dump(data, f, indent=2)
    return "Request submitted. Our team will respond within 30 days."
