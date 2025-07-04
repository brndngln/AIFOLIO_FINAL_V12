# Low-ticket upsell + high-ticket builder
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/marketing_log.json')

def build_email_sequence(product, ticket='low'):
    # Static, deterministic email sequence
    if ticket == 'low':
        sequence = [
            f"Welcome to {product['title']}! Here's how to get started.",
            "Unlock a bonus for your first purchase.",
            "Did you know? Upsize to Elite for more value!"
        ]
    else:
        sequence = [
            f"Elite Access: {product['title']} unlocks new profit streams.",
            "Case study: See how others scaled to $100K.",
            "Ready for high-ticket growth? Book your call."
        ]
    _log({'product': product['title'], 'ticket': ticket, 'timestamp': datetime.utcnow().isoformat(), 'type': 'email_sequence'})
    return sequence

def _log(entry):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(LOG_PATH, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass
