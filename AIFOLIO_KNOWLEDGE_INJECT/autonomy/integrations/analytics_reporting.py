import json
import datetime
import os

ANALYTICS_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/analytics_reporting_log.jsonl"
    )
)
os.makedirs(os.path.dirname(ANALYTICS_LOG), exist_ok=True)


def report_analytics(vault_id, metrics):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "vault_id": vault_id,
        "metrics": metrics,
        "status": "reported",
    }
    with open(ANALYTICS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
