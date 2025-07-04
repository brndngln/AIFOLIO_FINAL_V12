import os
import requests

def send_slack_alert(message: str, channel: str = None, username: str = None) -> bool:
    """
    Send an alert message to a Slack channel using an incoming webhook URL.
    Webhook URL should be set in the environment variable SLACK_WEBHOOK_URL.
    Optionally specify channel and username.
    Returns True if sent successfully, False otherwise.
    """
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        print("[Slack Alert] SLACK_WEBHOOK_URL not set in environment.")
        return False
    payload = {"text": message}
    if channel:
        payload["channel"] = channel
    if username:
        payload["username"] = username
    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        if response.status_code != 200:
            print(f"[Slack Alert] Failed to send alert: {response.status_code} {response.text}")
            return False
        return True
    except Exception as e:
        print(f"[Slack Alert] Exception: {e}")
        return False