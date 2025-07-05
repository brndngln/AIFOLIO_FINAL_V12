import os
import json
import datetime

HEALTH_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/delivery_health_log.jsonl")
)
os.makedirs(os.path.dirname(HEALTH_LOG), exist_ok=True)


# --- Delivery Health Monitor ---
def monitor_webhook_health(provider, status, latency=None):
    degraded = False
    if status != "ok" or (latency and latency > 5):
        degraded = True
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "provider": provider,
        "status": status,
        "latency": latency,
        "degraded": degraded,
    }
    with open(HEALTH_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


if __name__ == "__main__":
    print(monitor_webhook_health("Postmark", "ok", 0.3))
    print(monitor_webhook_health("Gumroad", "error", 10))
