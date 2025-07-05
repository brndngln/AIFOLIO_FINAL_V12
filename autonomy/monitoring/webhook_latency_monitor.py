import json
import datetime
import os

LATENCY_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/webhook_latency_log.jsonl")
)
os.makedirs(os.path.dirname(LATENCY_LOG), exist_ok=True)


def log_webhook_latency(webhook, latency, status):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "webhook": webhook,
        "latency": latency,
        "status": status,
    }
    with open(LATENCY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


if __name__ == "__main__":
    print(log_webhook_latency("postmark", 0.42, "ok"))
    print(log_webhook_latency("gumroad", 2.1, "slow"))
