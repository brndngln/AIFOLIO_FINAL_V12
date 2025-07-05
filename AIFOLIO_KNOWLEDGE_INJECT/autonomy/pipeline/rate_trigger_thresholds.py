"""
SAFE AI Rate-Based Trigger Thresholding
- Alerts on event spikes or error rate increases
- 100% static, config-driven, no adaptation
"""
import os
import json
import logging

THRESHOLD_CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "listeners/config/thresholds.json")
)
THRESHOLD_ALERT_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../analytics/threshold_alert_log.json")
)

os.makedirs(os.path.dirname(THRESHOLD_ALERT_LOG), exist_ok=True)


def check_event_rate(event_type, event_count, error_count):
    logger = logging.getLogger("rate_trigger_thresholds")
    if not os.path.exists(THRESHOLD_CONFIG_PATH):
        return False
    with open(THRESHOLD_CONFIG_PATH) as f:
        config = json.load(f)
    thresholds = config.get(event_type, {"max_events": 100, "max_errors": 5})
    alert = False
    if event_count > thresholds["max_events"] or error_count > thresholds["max_errors"]:
        alert = True
        with open(THRESHOLD_ALERT_LOG, "a") as f:
            f.write(
                json.dumps(
                    {
                        "event_type": event_type,
                        "event_count": event_count,
                        "error_count": error_count,
                        "alert": True,
                    }
                )
                + "\n"
            )
    return alert
