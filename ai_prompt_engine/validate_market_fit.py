# Create buyer personas, outcomes, frustrations, mini-win logic BEFORE generation starts
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/prompt_engine_log.json")


from typing import Dict, Any

def validate_market_fit(product: Dict[str, Any]) -> Dict[str, Any]:
    # Static, deterministic validation
    persona = {
        "persona": "Growth-Oriented Entrepreneur",
        "outcomes": ["More revenue", "Faster launches", "Better retention"],
        "frustrations": ["Low conversions", "Refunds", "Poor engagement"],
        "mini_win": "Achieve 10 sales in first week",
    }
    _log(
        {
            "product": product["title"],
            "timestamp": datetime.utcnow().isoformat(),
            "type": "market_fit",
        }
    )
    return persona


def _log(entry: Dict[str, Any]) -> None:
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
