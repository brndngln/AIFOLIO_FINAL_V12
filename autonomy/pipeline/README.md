# AIFOLIO™ Event Listener Dispatcher

## Overview
This dispatcher module ensures all event listeners are executed in strict, human-configurable priority order for every event in the AIFOLIO™ platform. It is fully deterministic, non-sentient, and retry-safe. No listener can block others unless explicitly required by configuration. All failures are logged, and the system is extensible for future integrations.

## Key Features
- **Priority Handling:** Listeners for each event are assigned a priority in `listener_config.json`. Lower numbers run first.
- **Retry-Safe:** Each listener is wrapped in a retry-safe queue (max 3 attempts, exponential backoff).
- **Audit Logging:** Every dispatch logs which listeners ran, in what order, and their success/failure.
- **No Sentience:** The dispatcher cannot learn or change priorities; all changes are via config or UI.
- **No Blocking:** Failures in one listener never block others (unless explicitly configured).
- **UI Preview:** Listener order for any event can be previewed in the dashboard.
- **Extensible:** Easy to add new listeners or integrations via config.

## How to Edit Listener Priorities
1. Open `listener_config.json`.
2. For each event type, edit the `priority` number for each listener (lower runs first).
3. Save the file. No code changes required.
4. (Optional) Use the dashboard UI to preview current order.

## Example: listener_config.json
```
{
  "vault_sold": [
    {"module": "vault_sold", "function": "handle_event", "priority": 10},
    {"module": "receipt_created", "function": "handle_event", "priority": 20}
  ]
}
```

## Example: Simulating a Vault Purchase Event
```
from dispatcher import EventListenerDispatcher

dispatcher = EventListenerDispatcher()
results = dispatcher.dispatch("vault_sold", {"vault_id": "V123", "user_id": "U456", "amount": 42.0})
for r in results:
    print(r)
```

## Safety & Best Practices
- **Never** edit code to change priorities—use the config file or UI only.
- The dispatcher will not generate or change listeners on its own.
- All failures are logged to `analytics/listener_audit_log.json`.
- The system is fully deterministic: same input = same output.
- Hooks for future integrations are present.

## Adding New Listeners
1. Implement the listener module in `autonomy/pipeline/listeners/`.
2. Add it to `listener_config.json` with the desired priority.
3. (Optional) Add UI preview.

---

**This system is 100% NON-SENTIENT and SAFE. All automation is deterministic and human-controlled.**
