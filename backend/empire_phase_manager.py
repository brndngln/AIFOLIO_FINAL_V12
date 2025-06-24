"""
AIFOLIO_FINAL_V12_EMPIRE_PHASE_MANAGER
Static, deterministic, SAFE AI-compliant Empire Phase Manager and Phase Alert System.
No sentience, no adaptive agents, fully human-controlled. All phase advancement requires explicit owner approval.
SAVE LABEL: AIFOLIO_FINAL_V12_EMPIRE_PHASE_MANAGER
"""
import logging
from backend.security.audit_logging import log_audit_event
logger = logging.getLogger(__name__)

# --- Empire Phase Manager ---
def get_empire_phase_status(vaults, revenue, current_phase_label):
    status = {
        'vault_count': len(vaults),
        'monthly_revenue': revenue,
        'empire_size': f"{len(vaults)} vaults, ${revenue}/mo",
        'active_phase_label': current_phase_label
    }
    log_audit_event(f"Empire Phase Status: {status}")
    return status

# --- Phase Alert System ---
def check_phase_ready_alerts(vaults, revenue, current_phase_label, phase_roadmap, owner_notify_callback):
    alerts = []
    for phase, conditions in phase_roadmap.items():
        if len(vaults) >= conditions['vaults'] and revenue >= conditions['revenue'] and current_phase_label != phase:
            alert = f"PHASE READY: You have {len(vaults)}+ vaults and ${revenue}/mo — {phase} now ready to run. Type: RUN {phase} to proceed."
            alerts.append(alert)
            log_audit_event(alert)
            owner_notify_callback(alert)
    if not alerts:
        log_audit_event("No phase ready alerts triggered.")
    return alerts

SAVE_LABEL = "AIFOLIO_FINAL_V12_EMPIRE_PHASE_MANAGER"
