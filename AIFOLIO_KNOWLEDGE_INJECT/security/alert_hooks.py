import os
import requests

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK_URL")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL")


def send_slack_alert(text):
    if not SLACK_WEBHOOK:
        return
    payload = {"text": text}
    try:
        requests.post(SLACK_WEBHOOK, json=payload, timeout=5)
    except Exception as e:
        print(f"[ALERT] Slack webhook failed: {e}")


def send_discord_alert(text):
    if not DISCORD_WEBHOOK:
        return
    payload = {"content": text}
    try:
        requests.post(DISCORD_WEBHOOK, json=payload, timeout=5)
    except Exception as e:
        print(f"[ALERT] Discord webhook failed: {e}")
