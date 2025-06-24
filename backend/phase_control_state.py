import json
import os
from datetime import datetime, timedelta

STATE_FILE = os.path.join(os.path.dirname(__file__), 'phase_control_state.json')

DEFAULT_STATE = {
    "phase": 12,
    "safe_mode": "ON",
    "last_upgrade": None,
    "next_upgrade": None,
    "system_integrity": "Verified",
    "lockdown": False
}

SAFE_AI_VERSION = "AIFOLIO_PHASE_CONTROL_STATE_V2_SAFEAI_FINAL"
SAFE_AI_COMPLIANT = True
OWNER_CONTROLLED = True
NON_SENTIENT = True

def _log_action(action, details, explanation, recommendation, priority):
    entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'action': action,
        'details': details,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }
    # Optional: persist audit log
    # with open('phase_control_audit_log.jsonl', 'a') as f:
    #     f.write(json.dumps(entry) + '\n')
    print(f"[AUDIT] {entry}")

def load_state():
    """
    Load current SAFE AI control state. Returns dict with state and SAFE AI metadata.
    """
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)
    explanation = "Loaded current system state."
    recommendation = None
    priority = 1
    _log_action('load_state', state, explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def save_state(state):
    """
    Save SAFE AI control state. Returns dict with confirmation and SAFE AI metadata.
    """
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)
    explanation = "State saved."
    recommendation = None
    priority = 1
    _log_action('save_state', state, explanation, recommendation, priority)
    return {
        'confirmation': True,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def update_phase(new_phase):
    """
    Update phase in SAFE AI control state. Returns dict with updated state and SAFE AI metadata.
    """
    state = load_state()['state']
    state["phase"] = new_phase
    save_state(state)
    explanation = f"Phase updated to {new_phase}."
    recommendation = None
    priority = 2
    _log_action('update_phase', new_phase, explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def toggle_safe_mode():
    """
    Toggle SAFE AI system safe mode. Returns dict with updated state and SAFE AI metadata.
    """
    state = load_state()['state']
    state["safe_mode"] = "OFF" if state["safe_mode"] == "ON" else "ON"
    save_state(state)
    explanation = f"Safe mode toggled to {state['safe_mode']}."
    recommendation = None
    priority = 3
    _log_action('toggle_safe_mode', state["safe_mode"], explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def trigger_upgrade():
    """
    Trigger SAFE AI upgrade. Returns dict with updated state and SAFE AI metadata.
    """
    state = load_state()['state']
    state["last_upgrade"] = datetime.utcnow().isoformat()
    state["next_upgrade"] = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    state["system_integrity"] = "Verified"
    save_state(state)
    explanation = "Upgrade triggered. Next scheduled in 24h."
    recommendation = "Review system after upgrade."
    priority = 2
    _log_action('trigger_upgrade', state, explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def lockdown_system():
    """
    Lockdown SAFE AI system. Returns dict with updated state and SAFE AI metadata.
    """
    state = load_state()['state']
    state["lockdown"] = True
    state["system_integrity"] = "Action Needed"
    save_state(state)
    explanation = "System lockdown activated."
    recommendation = "Resolve issues before releasing lockdown."
    priority = 10
    _log_action('lockdown_system', state, explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

def release_lockdown():
    """
    Release SAFE AI system lockdown. Returns dict with updated state and SAFE AI metadata.
    """
    state = load_state()['state']
    state["lockdown"] = False
    state["system_integrity"] = "Verified"
    save_state(state)
    explanation = "System lockdown released."
    recommendation = None
    priority = 1
    _log_action('release_lockdown', state, explanation, recommendation, priority)
    return {
        'state': state,
        'explanation': explanation,
        'recommendation': recommendation,
        'priority': priority,
        'version': SAFE_AI_VERSION,
        'SAFE_AI_COMPLIANT': SAFE_AI_COMPLIANT,
        'OWNER_CONTROLLED': OWNER_CONTROLLED,
        'NON_SENTIENT': NON_SENTIENT
    }

# --- Static Drift/Hallucination Protection (stub) ---
def control_drift_protection():
    return {"drift": False, "explanation": "No drift detected."}

# --- Static Feedback Loop (stub, not user learned) ---
def control_static_feedback():
    return ["Review state transitions and audit logs for compliance."]

# --- Extension Point: Add future static SAFE AI features here ---
