"""
AIFOLIO™ SAFE AI MODULE: Telegram Alert Stub
- Static, non-sentient
- Logs alert events to Telegram (stub only, no real integration)
- No autonomous alert escalation
"""
import logging

LOG_PATH = "../../distribution/legal_exports/telegram_alert_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def log_telegram_alert(message):
    logging.info(f"Telegram alert (stub): {message}")
