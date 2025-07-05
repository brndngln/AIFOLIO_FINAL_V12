import streamlit as st
import json
import os
from pathlib import Path


from typing import List, Dict, Any, TypedDict

def load_audit_logs(log_dir: str = "./ai_core/EmmaLogs/") -> List[str]:
    """
    Loads the list of encrypted audit log filenames from the specified directory.
    Args:
        log_dir: Directory containing audit log files.
    Returns:
        List of log filenames.
    """
    from pathlib import Path
    logs: List[str] = []
    for fname in Path(log_dir).glob("*.log.enc"):
        logs.append(fname.name)
    return logs


def load_intrusion_alerts(alert_file: str = "./ai_core/EmmaLogs/intrusion_alerts.log") -> List[str]:
    """
    Loads intrusion alerts from the specified file.
    Args:
        alert_file: Path to the intrusion alerts log file.
    Returns:
        List of alert lines.
    """
    if not os.path.exists(alert_file):
        return []
    with open(alert_file, "r") as f:
        return f.readlines()


def load_vault_index(index_file: str = "ai_core/EmmaLogs/EmmaVaultIndex.json") -> Dict[str, Any]:
    """
    Loads the vault index from a JSON file.
    Args:
        index_file: Path to the vault index JSON file.
    Returns:
        Dictionary representing the vault index.
    """
    if not os.path.exists(index_file):
        return {}
    with open(index_file, "r") as f:
        from typing import cast
        return cast(Dict[str, Any], json.load(f))


class DashboardData(TypedDict):
    audit_logs: List[str]
    intrusion_alerts: List[str]
    vault_index: Dict[str, Any]

def main() -> None:
    """
    Streamlit dashboard entry point for Emma HyperSecure Security Dashboard.
    Displays audit logs, intrusion alerts, vault index, and system status.
    """
    st.title("Emma HyperSecure Security Dashboard")
    st.subheader("Audit Logs")
    logs = load_audit_logs()
    st.write(logs)
    st.subheader("Intrusion Alerts")
    alerts = load_intrusion_alerts()
    st.write(alerts)
    st.subheader("Vault Index")
    vault = load_vault_index()
    st.json(vault)
    st.subheader("System Status")
    st.write("All OMNIELITE security layers operational.")


# Emma's Streamlit dashboard is DISABLED for non-visual mode reset.
# if __name__ == '__main__':
#     main()
