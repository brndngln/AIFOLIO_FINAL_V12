# Upgrades tone, hooks, niche alignment for product copy
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/marketing_log.json")


def generate_copy(product, tone="elite", hook="profit", niche="general"):
    # Static, deterministic copy upgrade
    copy = f"[{tone.upper()}] {product['title']} — {hook.title()} for {niche.title()}\n{product['description']}\nCTA: {product.get('cta', 'Unlock now!')}"
    _log(
        {
            "product": product["title"],
            "tone": tone,
            "hook": hook,
            "niche": niche,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    return copy


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
