import os
import json
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/usage_anomalies.json")
USAGE_PATH = os.path.join(os.path.dirname(__file__), "../logs/usage_metrics.json")
SPIKE_FACTOR = 2  # 2x over 7-day avg


# Log usage (call this from each API endpoint that uses a secret)
def log_usage(key, count=1):
    if os.path.exists(USAGE_PATH):
        with open(USAGE_PATH, "r") as f:
            usage = json.load(f)
    else:
        usage = {}
    day = datetime.utcnow().strftime("%Y-%m-%d")
    if key not in usage:
        usage[key] = {}
    usage[key][day] = usage[key].get(day, 0) + count
    with open(USAGE_PATH, "w") as f:
        json.dump(usage, f, indent=2)


# Check for spikes (run as background job)
def check_for_spikes():
    if not os.path.exists(USAGE_PATH):
        return []
    with open(USAGE_PATH, "r") as f:
        usage = json.load(f)
    anomalies = []
    for key, days in usage.items():
        sorted_days = sorted(days.keys())[-8:]
        if len(sorted_days) < 2:
            continue
        last_day = sorted_days[-1]
        last_val = days[last_day]
        avg = sum([days[d] for d in sorted_days[:-1]]) / max(1, len(sorted_days) - 1)
        if avg > 0 and last_val > SPIKE_FACTOR * avg:
            anomaly = {
                "key": key,
                "timestamp": datetime.utcnow().isoformat(),
                "avg": avg,
                "current": last_val,
                "factor": last_val / avg,
                "event": "spike_detected",
            }
            anomalies.append(anomaly)
            log_anomaly(anomaly)
    return anomalies


def log_anomaly(anomaly):
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(anomaly)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
