# core/integrations/discord_notifier.py
import requests


def send_discord_alert(webhook_url, message):
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    response.raise_for_status()
