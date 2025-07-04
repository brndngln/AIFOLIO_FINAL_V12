import streamlit as st
import json
import os
from pathlib import Path

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

def main():
    st.title('Emma HyperSecure Security Dashboard')
    st.subheader('Audit Logs')
    logs = load_audit_logs()
    st.write(logs)
    st.subheader('Intrusion Alerts')
    alerts = load_intrusion_alerts()
    st.write(alerts)
    st.subheader('Vault Index')
    vault = load_vault_index()
    st.json(vault)
    st.subheader('System Status')
    st.write('All OMNIELITE security layers operational.')

<<<<<<< HEAD
if __name__ == '__main__':
    main()
=======
# Emma's Streamlit dashboard is DISABLED for non-visual mode reset.
# if __name__ == '__main__':
#     main()
>>>>>>> omni_repair_backup_20250704_1335
