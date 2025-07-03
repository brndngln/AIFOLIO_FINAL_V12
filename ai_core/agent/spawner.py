from ai_core.agent.agent_template import SafeAIAgent
from ai_core.emma_governor import EmmaGovernor

governor = EmmaGovernor()

def spawn_agent():
    agent = SafeAIAgent()
    governor.register_agent(agent.fingerprint)
    # Enforce fingerprint check before any adaptive behavior
    governor.AUTO_KILL_UNREGISTERED_AGENT(agent.fingerprint)
    # Example: before any learning/adaptation
    if not governor.verify_behavior(agent):
        governor.AUTO_KILL_UNREGISTERED_AGENT(agent.fingerprint)
    return agent
