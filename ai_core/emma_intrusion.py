import os
import time
import getpass
from typing import Any, Dict

INTRUSION_LOG = "ai_core/EmmaLogs/intrusion_alerts.log"

import requests


def log_intrusion(event: str, filename: str) -> None:
    """
    Logs an intrusion event to the intrusion log and sends a webhook alert if configured.
    Args:
        event: The event type (e.g., 'PERMISSION_CHANGE').
        filename: The file involved in the event.
    """
    user: str = getpass.getuser()
    ts: str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    msg: str = f"{ts} | {user} | {event} | {filename}\n"
    with open(INTRUSION_LOG, "a") as f:
        f.write(msg)
    # SIEM/webhook integration (example: replace with your endpoint)
    try:
        webhook_url = os.environ.get("EMMA_SIEM_WEBHOOK")
        if webhook_url:
            requests.post(webhook_url, json={"alert": msg})
    except Exception as e:
        print(f"Webhook/SIEM integration failed: {e}")
    print(f"INTRUSION ALERT: {msg}")


def hsm_sign(data: Any) -> None:
    """
    Stub for HSM signing.
    Args:
        data: Data to be signed.
    """
    pass


def airgap_transfer(file_path: str) -> None:
    """
    Stub for secure transfer to air-gapped storage.
    Args:
        file_path: Path to the file to transfer.
    """
    pass


def monitor_permissions(log_dir: str = "ai_core/EmmaLogs/") -> None:
    """
    Monitors for unauthorized chmod/chown or access attempts in the log directory.
    Args:
        log_dir: Directory to monitor.
    """
    last_perms: Dict[str, str] = {}
    while True:
        for fname in os.listdir(log_dir):
            path = os.path.join(log_dir, fname)
            try:
                perms = oct(os.stat(path).st_mode)[-3:]
                if fname not in last_perms:
                    last_perms[fname] = perms
                elif perms != last_perms[fname]:
                    log_intrusion("PERMISSION_CHANGE", fname)
                    last_perms[fname] = perms
            except Exception:
                continue
        time.sleep(10)
