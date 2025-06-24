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

def load_state():
    if not os.path.exists(STATE_FILE):
        save_state(DEFAULT_STATE)
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def update_phase(new_phase):
    state = load_state()
    state["phase"] = new_phase
    save_state(state)

def toggle_safe_mode():
    state = load_state()
    state["safe_mode"] = "OFF" if state["safe_mode"] == "ON" else "ON"
    save_state(state)
    return state["safe_mode"]

def trigger_upgrade():
    state = load_state()
    state["last_upgrade"] = datetime.utcnow().isoformat()
    # Next upgrade scheduled 24h later, or manual
    state["next_upgrade"] = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    state["system_integrity"] = "Verified"
    save_state(state)

def lockdown_system():
    state = load_state()
    state["lockdown"] = True
    state["system_integrity"] = "Action Needed"
    save_state(state)

def release_lockdown():
    state = load_state()
    state["lockdown"] = False
    state["system_integrity"] = "Verified"
    save_state(state)
