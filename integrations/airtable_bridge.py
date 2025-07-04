import os
import requests
import logging

def send_airtable_record(payload):
    url = os.getenv('AIRTABLE_API_URL')
    token = os.getenv('AIRTABLE_API_TOKEN')
    if not url or not token:
        logging.warning('Airtable API url/token missing')
        return
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Airtable record failed: {e}")
