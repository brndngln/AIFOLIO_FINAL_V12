import requests
import json
import datetime
import os

HEALTH_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../analytics/api_latency_health_monitor_log.jsonl",
    )
)
os.makedirs(os.path.dirname(HEALTH_LOG), exist_ok=True)


# --- AI API Latency/Health Monitor (Static, Non-Learning) ---
def check_api_health(api_name, url, timeout=10):
    try:
        start = datetime.datetime.utcnow()
        resp = requests.get(url, timeout=timeout)
        end = datetime.datetime.utcnow()
        latency = (end - start).total_seconds()
        status = resp.status_code
        ok = status == 200
    except Exception as e:
        latency = None
        status = f"error: {e}"
        ok = False
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "api_name": api_name,
        "url": url,
        "status": status,
        "latency": latency,
        "ok": ok,
    }
    with open(HEALTH_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return ok, latency, status
