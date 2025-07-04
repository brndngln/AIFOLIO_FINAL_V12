"""
AIFOLIO SAFE AI Webhook/Notification Integration
Static, deterministic notification hooks for vault events (Slack, Discord, Email).
All secrets/configs via environment variables. No adaptive logic.
"""
import os
import logging
import requests
logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
EMAIL_NOTIFICATION_ADDRESS = os.getenv("AIFOLIO_NOTIFICATION_EMAIL")


def notify_slack(message: str) -> bool:
    """Send static notification to Slack webhook. Extension: real Slack integration."""
    if not SLACK_WEBHOOK_URL:
        logger.info("SLACK_WEBHOOK_URL not set. Skipping Slack notification.")
        return False
    payload = {"text": message}
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload)
        logger.info(f"Slack notification sent: {message}")
        return resp.status_code == 200
    except Exception as e:
        logger.error(f"Slack notification failed: {e}")
        return False

def notify_discord(message: str) -> bool:
    """Send static notification to Discord webhook. Extension: real Discord integration."""
    if not DISCORD_WEBHOOK_URL:
        logger.info("DISCORD_WEBHOOK_URL not set. Skipping Discord notification.")
        return False
    payload = {"content": message}
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        logger.info(f"Discord notification sent: {message}")
        return resp.status_code == 204
    except Exception as e:
        logger.error(f"Discord notification failed: {e}")
        return False

def notify_email(subject: str, body: str) -> bool:
    """Static stub for email notification. Extension: real email integration."""
    if not EMAIL_NOTIFICATION_ADDRESS:
        logger.info("EMAIL_NOTIFICATION_ADDRESS not set. Skipping email notification.")
        return False
    logger.info(f"Static email notification: {subject} to {EMAIL_NOTIFICATION_ADDRESS}")
    # Extension: Integrate with real email service
    return True
