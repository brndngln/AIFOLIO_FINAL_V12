import os
import time
import logging
import getpass

INTRUSION_LOG = 'ai_core/EmmaLogs/intrusion_alerts.log'

def log_intrusion(event, filename):
    user = getpass.getuser()
    ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    msg = f'{ts} | {user} | {event} | {filename}\n'
    with open(INTRUSION_LOG, 'a') as f:
        f.write(msg)
    # Optional: integrate with real alerting (email, webhook, SIEM)
    print(f'INTRUSION ALERT: {msg}')

def monitor_permissions(log_dir='ai_core/EmmaLogs/'):
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
                    log_intrusion('PERMISSION_CHANGE', fname)
                    last_perms[fname] = perms
            except Exception:
                continue
        time.sleep(10)
