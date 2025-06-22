import requests
import json
import os
from datetime import datetime

WEBHOOK_URLS = [
    os.getenv("NOTION_WEBHOOK_URL"),
    os.getenv("AIRTABLE_WEBHOOK_URL"),
    os.getenv("SLACK_WEBHOOK_URL")
]

def notify_policy_change(policy_name: str, version_hash: str, timestamp: str):
    """
    Notify external tools when a policy changes.
    """
    payload = {
        "policy_name": policy_name,
        "version_hash": version_hash,
        "timestamp": timestamp
    }
    for url in WEBHOOK_URLS:
        if url:
            try:
                requests.post(url, json=payload, timeout=6)
            except Exception as e:
                print(f"Webhook notification failed for {url}: {e}")
