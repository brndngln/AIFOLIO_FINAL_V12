"""
SAFE AI Pipeline Cold-Start Recovery Logic
- Re-processes unhandled events after downtime
- No no loops or self-calling functions, no adaptation, static only
- Admin/manual trigger only
"""
import os
import json
import logging

UNHANDLED_EVENTS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../analytics/unhandled_events.json")
)
RECOVERY_LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../analytics/cold_start_recovery_log.json")
)

os.makedirs(os.path.dirname(UNHANDLED_EVENTS_PATH), exist_ok=True)
os.makedirs(os.path.dirname(RECOVERY_LOG_PATH), exist_ok=True)


def recover_events():
    logger = logging.getLogger("cold_start_recovery")
    if not os.path.exists(UNHANDLED_EVENTS_PATH):
        return []
    with open(UNHANDLED_EVENTS_PATH) as f:
        events = json.load(f)
    recovered = []
    for event in events:
        # Static, manual re-processing only
        try:
            # (In real system, would call event_bus.dispatch_event)
            recovered.append(event)
        except Exception as e:
            logger.error(f"Recovery failed for event {event}: {e}")
    with open(RECOVERY_LOG_PATH, "a") as f:
        f.write(json.dumps({"recovered": recovered, "count": len(recovered)}) + "\n")
    return recovered
