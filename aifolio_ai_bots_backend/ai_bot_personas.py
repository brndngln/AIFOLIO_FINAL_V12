"""
AIFOLIO™ AI Bot Personas & Containment
Defines all bot roles, enforces command-only mode, logs all actions, and disables sentient/adaptive logic.
"""
import logging

BOT_PERSONAS = {
    "pdf_bot": "The Editor-in-Genius",
    "cover_bot": "Aesthetic Overlord",
    "vault_strategist": "The Empire Cartographer",
    "monetization_bot": "The Closer",
    "compliance_bot": "The Enforcer",
}

STRICT_COMMAND_MODE = True


def log_bot_action(bot, action, details=None):
    logging.info(f"[BOT LOG] {bot}: {action} | {details}")


def enforce_bot_laws(bot, action):
    if not STRICT_COMMAND_MODE:
        raise RuntimeError("Bots must operate in command-only mode.")
    if "memory" in action or "chain" in action or "loop" in action:
        raise RuntimeError("No memory chains, loops, or sentient logic allowed.")
    log_bot_action(bot, action)
    return True
