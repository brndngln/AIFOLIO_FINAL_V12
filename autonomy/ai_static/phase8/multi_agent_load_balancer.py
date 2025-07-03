"""
SAFE AI Static Module: Multi-Agent Load-Balancer (Pre-Configured)
- Logs static, preconfigured load-balancing events
- No dynamic, learning, or autonomous behavior (static, preconfigured only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/multi_agent_load_balancer_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

AGENTS = ["agent_a", "agent_b", "agent_c"]
TASKS = ["vault_audit", "policy_check", "market_scan"]


def log_balancer_event(agent, task, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] LOAD-BALANCER: {agent} | Task: {task} | Triggered by: {triggered_by}"
    logging.info(event)
    return event


def run_static_load_balancing(triggered_by):
    for i, task in enumerate(TASKS):
        agent = AGENTS[i % len(AGENTS)]
        log_balancer_event(agent, task, triggered_by)
    return "Static multi-agent load balancing logged."
