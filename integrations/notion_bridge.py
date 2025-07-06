import os
import requests
import logging


from typing import Dict, Any

def send_notion_task(payload: Dict[str, Any]) -> None:
    """
    Send a task to Notion using the provided payload.
    Args:
        payload: The task data as a dictionary.
    """
    url = os.getenv("NOTION_API_URL")
    token = os.getenv("NOTION_API_TOKEN")
    if not url or not token:
        logging.warning("Notion API url/token missing")
        return
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Notion task failed: {e}")
