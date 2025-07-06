from ai_core.agent.agent_template import SafeAIAgent
from ai_core.emma_governor import EmmaGovernor

governor = EmmaGovernor()


from typing import Any

def spawn_agent() -> Any:
    """
    Spawns a new SAFE AI agent and performs strict registration and verification.
    Returns:
        The spawned SafeAIAgent instance.
    """
    agent = SafeAIAgent()
    governor.register_agent(agent.fingerprint)
    # Enforce fingerprint check before any adaptive behavior
    governor.AUTO_KILL_UNREGISTERED_AGENT(agent.fingerprint)
    # Example: before any learning/adaptation
    governor.verify_behavior(agent)
    return agent
