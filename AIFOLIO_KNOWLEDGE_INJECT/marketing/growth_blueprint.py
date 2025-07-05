# “Zero to $100K” strategy per product
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/marketing_log.json")


def growth_blueprint(product):
    # Static, deterministic blueprint
    steps = [
        "Define target outcome",
        "Build high-converting funnel",
        "Leverage social proof",
        "Run retargeting ads",
        "Launch to warm audience",
        "Optimize for LTV",
        "Automate testimonials",
        "Scale with partnerships",
    ]
    plan = {
        "product": product["title"],
        "steps": steps,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _log(plan)
    return plan


def _log(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass
