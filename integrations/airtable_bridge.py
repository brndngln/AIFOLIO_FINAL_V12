import os
import requests
import logging


from typing import Dict, Any

def send_airtable_record(payload: Dict[str, Any]) -> None:
    """
    Send a record to Airtable using the provided payload.
    Args:
        payload: The record data as a dictionary.
    """
    url = os.getenv("AIRTABLE_API_URL")
    token = os.getenv("AIRTABLE_API_TOKEN")
    if not url or not token:
        logging.warning("Airtable API url/token missing")
        return
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Airtable record failed: {e}")
