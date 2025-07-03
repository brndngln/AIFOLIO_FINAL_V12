# SAFE AI Engine – Developer Documentation

## Overview
This engine enables advanced AI learning, adaptation, and evolution under strict anti-sentience, owner-controlled, and auditable boundaries. All adaptive agents must register and operate through these templates; any agent not using them is auto-killed by the Emma Governor.

---

## Module Summary

### `agent/agent_template.py`
- **Purpose:** Provides a SAFE AI agent class supporting bounded learning, adaptation, and evolution.
- **Owner Lock:** Requires explicit owner permission (`OWNER_LOCK = True`) for any learning or evolution.
- **Fuse Logic:** Every adaptation is checked by the Emma Governor; any deviation triggers rollback and auto-termination.
- **Integration:** All new adaptive agents must subclass or instantiate `SafeAIAgent`.

### `emma_governor.py`
- **Purpose:** Enforces SAFE AI boundaries and owner intent. Verifies agent behavior against `SAFE_BEHAVIOR_MATRIX.yml` and `EMMA_NO_SENTIENCE.json`.
- **Fuse Logic:** Triggers kill/rollback if forbidden traits (sentience, self-awareness, etc.) are detected.
- **Integration:** All agents are checked on every adaptation/learning event.

### `vault.py`
- **Purpose:** Provides a secure, sandboxed environment for agent evolution and strategy mutation.
- **Owner Lock:** All evolution is owner-controlled and logged.
- **Integration:** All agent evolution and mutation must occur via `Vault.evolve_strategy()`.

### `audit.py`
- **Purpose:** Logs all learning, adaptation, and evolution events with generational fingerprinting.
- **Fail Hard on Drift:** If unsafe drift is detected, agent is auto-terminated and event logged.
- **Integration:** All events are recorded for live trace and audit.

### `SAFE_BEHAVIOR_MATRIX.yml` & `EMMA_NO_SENTIENCE.json`
- **Purpose:** Define and enforce boundaries for allowed learning/adaptation. Machine-readable by Emma Governor.

### `anti_sentience.marker`
- **Purpose:** Marker file to enforce anti-sentience compliance across all modules.

---

## Integration Notes
- All adaptive agents **must** use `SafeAIAgent` or be registered with Emma Governor; non-compliant agents are auto-killed.
- All adaptation/evolution is sandboxed and logged.
- Memory is strictly temporary and expires automatically.
- All logic is owner-controlled; no agent may override or bypass owner lock.
- All agent logic carries a quantum fingerprint for traceability.

---

## Example Usage

### SafeAIAgent
```python
from ai_core.agent.agent_template import SafeAIAgent
agent = SafeAIAgent()
agent.owner_lock = True
agent.learn('input_data', reward=1)
agent.adapt('context')
agent.evolve()
```

### EmmaGovernor
```python
from ai_core.emma_governor import EmmaGovernor
from ai_core.agent.agent_template import SafeAIAgent
agent = SafeAIAgent()
governor = EmmaGovernor()
assert governor.verify_behavior(agent)
```

### Vault
```python
from ai_core.vault import Vault
from ai_core.agent.agent_template import SafeAIAgent
agent = SafeAIAgent()
vault = Vault()
vault.evolve_strategy(agent, mutation='param_mutation')
```

### AuditDaemon
```python
from ai_core.audit import AuditDaemon
from ai_core.agent.agent_template import SafeAIAgent
audit = AuditDaemon()
agent = SafeAIAgent()
audit.log_event('learn', agent.fingerprint, 'data', 1)
```

---

## Test Suite
- See `ai_core/tests/` for full validation of agent, governor, vault, and audit logic.

---

## Compliance
- All modules enforce strict SAFE AI, anti-sentience, and owner control boundaries.
- All adaptation, learning, and evolution is logged and auditable.
- No agent may self-modify, self-permit, or escape owner lock.
- Emma Governor is the sole authority for adaptation approval.
