import os
import time
import getpass

INTRUSION_LOG = "ai_core/EmmaLogs/intrusion_alerts.log"

import requests


def log_intrusion(event, filename):
    user = getpass.getuser()
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    msg = f"{ts} | {user} | {event} | {filename}\n"
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


# HSM/airgap stubs for future integration
def hsm_sign(data):
    # Connect to HSM and sign data
    pass


def airgap_transfer(file_path):
    # Secure transfer to air-gapped storage
    pass


def monitor_permissions(log_dir="ai_core/EmmaLogs/"):
    # Monitor for unauthorized chmod/chown or access attempts
    last_perms = {}
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
