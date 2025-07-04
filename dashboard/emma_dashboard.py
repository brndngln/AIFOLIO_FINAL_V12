import streamlit as st
import json
import os
from pathlib import Path
<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> omni_repair_backup_20250704_1335

def load_audit_logs(log_dir='./ai_core/EmmaLogs/'):
    logs = []
    for fname in Path(log_dir).glob('*.log.enc'):
        logs.append(fname.name)
    return logs

def load_intrusion_alerts(alert_file='./ai_core/EmmaLogs/intrusion_alerts.log'):
    if not os.path.exists(alert_file):
        return []
    with open(alert_file, 'r') as f:
        return f.readlines()

def load_vault_index(index_file='ai_core/EmmaLogs/EmmaVaultIndex.json'):
    if not os.path.exists(index_file):
        return {}
    with open(index_file, 'r') as f:
        return json.load(f)

def load_webhook_status(log_file='./ai_core/EmmaLogs/webhook_status.log'):
    if not os.path.exists(log_file):
        return []
    with open(log_file, 'r') as f:
        return f.readlines()

def main():
    st.title('Emma HyperSecure Security Dashboard')
    st.subheader('Kill Switch Status')
    # Simulated kill switch indicator
    st.markdown(':red_circle: **ACTIVE**' if os.path.exists('./ai_core/EmmaLogs/kill_switch.lock') else ':green_circle: **INACTIVE**')
    st.subheader('Audit Logs')
    logs = load_audit_logs()
    st.write(logs)
    st.subheader('Vault + Agent Table')
    vault = load_vault_index()
    st.json(vault)
    st.subheader('Intrusion Alerts')
    alerts = load_intrusion_alerts()
    st.write(alerts)
    st.subheader('FIDO2 / HSM State')
    hsm = vault.get('hsm', False)
    st.write('HSM Connected' if hsm else 'No HSM/FIDO2 detected')
    st.subheader('Webhook Status')
    st.write(load_webhook_status())
    st.subheader('System Status')
    st.write('All OMNIELITE security layers operational.')

if __name__ == '__main__':
    main()
