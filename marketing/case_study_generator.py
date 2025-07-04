# 3-part storytelling with CTA
import json
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), '../logs/marketing_log.json')

def generate_case_study(product):
    # Static, deterministic case study
    case = {
        'intro': f"How {product['title']} solved a real-world challenge.",
        'story': f"User applied {product['title']} and saw measurable results.",
        'cta': f"Ready to achieve similar results? {product.get('cta', 'Unlock now!')}"
    }
    _log({'product': product['title'], 'timestamp': datetime.utcnow().isoformat(), 'type': 'case_study'})
    return case

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
