"""
Elite Heartbeat and Compliance Export Scheduler for AIFOLIO™
- Schedules daily heartbeat to admin and daily compliance export to Notion/Sheets/Airtable
- SAFE AI, deterministic, owner-controlled, auditable
"""
import os
import time
import requests
<<<<<<< HEAD
import json
from datetime import datetime, timedelta
=======
from datetime import datetime
>>>>>>> omni_repair_backup_20250704_1335
from threading import Thread

ADMIN_HEARTBEAT_URL = os.getenv('ADMIN_HEARTBEAT_URL')
COMPLIANCE_EXPORT_URL = os.getenv('COMPLIANCE_EXPORT_URL', 'http://localhost:8000/api/export/compliance')
EXPORT_TARGETS = ['notion', 'sheets', 'airtable']
LOG_PATH = 'logs/compliance/export_scheduler.log'

LAST_HEARTBEAT_FILE = 'logs/compliance/last_heartbeat.txt'
LAST_EXPORT_FILE = 'logs/compliance/last_export.txt'

HEARTBEAT_HOUR = 8  # 8 AM UTC
EXPORT_HOUR = 9      # 9 AM UTC


def log_event(msg):
    with open(LOG_PATH, 'a') as f:
        f.write(f"{datetime.utcnow().isoformat()} | {msg}\n")

def send_heartbeat():
    payload = {'status': 'alive', 'timestamp': datetime.utcnow().isoformat()}
    try:
        if ADMIN_HEARTBEAT_URL:
            requests.post(ADMIN_HEARTBEAT_URL, json=payload, timeout=5)
        with open(LAST_HEARTBEAT_FILE, 'w') as f:
            f.write(payload['timestamp'])
        log_event('Heartbeat sent')
    except Exception as e:
        log_event(f'Heartbeat failed: {e}')

def export_compliance():
    for target in EXPORT_TARGETS:
        try:
            res = requests.get(f"{COMPLIANCE_EXPORT_URL}?type={target}", timeout=10)
            result = res.json()
            log_event(f"Compliance export to {target}: {result['status']}")
        except Exception as e:
            log_event(f"Compliance export to {target} failed: {e}")
    with open(LAST_EXPORT_FILE, 'w') as f:
        f.write(datetime.utcnow().isoformat())

def scheduler_loop():
    while True:
        now = datetime.utcnow()
        # Heartbeat
        if now.hour == HEARTBEAT_HOUR and (not os.path.exists(LAST_HEARTBEAT_FILE) or (datetime.utcnow() - datetime.fromisoformat(open(LAST_HEARTBEAT_FILE).read().strip())).days >= 1):
            send_heartbeat()
        # Compliance export
        if now.hour == EXPORT_HOUR and (not os.path.exists(LAST_EXPORT_FILE) or (datetime.utcnow() - datetime.fromisoformat(open(LAST_EXPORT_FILE).read().strip())).days >= 1):
            export_compliance()
        time.sleep(3600)  # Check every hour

def start_scheduler():
    Thread(target=scheduler_loop, daemon=True).start()

if __name__ == '__main__':
    start_scheduler()
    while True:
        time.sleep(3600)
