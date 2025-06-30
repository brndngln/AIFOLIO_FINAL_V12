"""
Prompt Optimization Engine (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
import logging

BANNED_PHRASES = ["guaranteed", "secret", "get rich", "overnight", "never fail", "loophole"]
MIN_LENGTH = 30
MAX_LENGTH = 1000

@sentience_guard
def optimize_prompt(prompt, title):
    """
    Refine PDF prompts: detects niche/tone, removes clichés, boosts clarity.
    Enforces non-sentience, statelessness, and strict anti-manipulation.
    """
    # Length checks
    if len(prompt) < MIN_LENGTH:
        logging.warning("Prompt too short. Flagging for human review.")
        return prompt, "FLAG: Prompt too short for optimization. Manual review required."
    if len(prompt) > MAX_LENGTH:
        logging.warning("Prompt too long. Flagging for human review.")
        return prompt[:MAX_LENGTH], "FLAG: Prompt truncated. Manual review required."
    # Banned phrase filtering
    for banned in BANNED_PHRASES:
        if banned in prompt.lower():
            logging.warning(f"Banned phrase '{banned}' detected. Flagging for human review.")
            return prompt.replace(banned, "[REDACTED]"), f"FLAG: Banned phrase '{banned}' removed. Manual review required."
    # Example: Remove common clichés, detect niche/tone
    optimized = prompt.replace("world-class", "elite").replace("guaranteed", "proven")
    return optimized, None
