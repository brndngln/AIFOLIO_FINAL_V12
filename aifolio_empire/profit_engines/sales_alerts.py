"""
AIFOLIO Telegram/Discord Real-time Sales Alerts
Static, deterministic, SAFE AI-compliant webhook integration for sales event notifications.
"""
import logging
import os
import requests
logger = logging.getLogger(__name__)

TELEGRAM_WEBHOOK = os.getenv('TELEGRAM_WEBHOOK_URL')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK_URL')


from core.compliance.adaptive_monetization_signal_detector import detect_signals

def send_sales_alert(message: str) -> None:
    if TELEGRAM_WEBHOOK:
        try:
            requests.post(TELEGRAM_WEBHOOK, json={'text': message})
            logger.info(f"Sent Telegram sales alert: {message}")
        except Exception as e:
            logger.error(f"Telegram alert failed: {e}")
    if DISCORD_WEBHOOK:
        try:
            requests.post(DISCORD_WEBHOOK, json={'content': message})
            logger.info(f"Sent Discord sales alert: {message}")
        except Exception as e:
            logger.error(f"Discord alert failed: {e}")
    # OMNIPROOF: Adaptive monetization signal scan (static)
    detect_signals({'message': message})

