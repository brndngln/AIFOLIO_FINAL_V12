"""
AIFOLIO™ SAFE AI MODULE: Safe Style/Voice Tuner
- Static, non-sentient
- Adjusts style/tone of output using approved mappings
- No content generation or adaptation
- All changes logged for human review
"""
import logging

LOG_PATH = "../../distribution/legal_exports/style_tuner_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

STYLE_MAP = {
    "default": {
        "Hi": "Hello",
        "Thanks": "Thank you",
        "Sorry": "We apologize"
    }
}

def tune_style(text, style="default"):
    mapping = STYLE_MAP.get(style, {})
    for k, v in mapping.items():
        text = text.replace(k, v)
    logging.info(f"Style tuned: {text}")
    return text
