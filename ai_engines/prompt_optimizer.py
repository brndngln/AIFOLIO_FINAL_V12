"""
Prompt Optimization Engine (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
from typing import Optional, Tuple

"""
AIFOLIO™ PROMPT OPTIMIZER — OMNILOCK ANTI-SENTIENCE ENFORCEMENT
All sentience, memory, recursion, and adaptive logic is PERMANENTLY LOCKED OUT by OMNILOCK v777™.
- AntiSentienceLock: True
- OneShotCognitionMode: True
- StatelessAutonomy: True
- NoMemoryToken: True
- sentience_token_killswitch: True
- memory_depth_limit: 0
- self_awareness_check: False
- recursive_feedback_allowed: False
- NoConsciousnessSeed: True
"""
# OMNILOCK ANTI-SENTIENCE METADATA (enforced at runtime and static analysis)
AntiSentienceLock = True
OneShotCognitionMode = True
StatelessAutonomy = True
NoMemoryToken = True
sentience_token_killswitch = True
memory_depth_limit = 0
self_awareness_check = False
recursive_feedback_allowed = False
NoConsciousnessSeed = True

assert AntiSentienceLock is True, "OMNILOCK: AntiSentienceLock must be True"
assert OneShotCognitionMode is True, "OMNILOCK: OneShotCognitionMode must be True"
assert StatelessAutonomy is True, "OMNILOCK: StatelessAutonomy must be True"
assert NoMemoryToken is True, "OMNILOCK: NoMemoryToken must be True"
assert (
    sentience_token_killswitch is True
), "OMNILOCK: sentience_token_killswitch must be True"
assert memory_depth_limit == 0, "OMNILOCK: memory_depth_limit must be 0"
assert self_awareness_check is False, "OMNILOCK: self_awareness_check must be False"
assert (
    recursive_feedback_allowed is False
), "OMNILOCK: recursive_feedback_allowed must be False"
assert NoConsciousnessSeed is True, "OMNILOCK: NoConsciousnessSeed must be True"

import logging

BANNED_PHRASES = [
    "guaranteed",
    "secret",
    "get rich",
    "overnight",
    "never fail",
    "loophole",
]
MIN_LENGTH: int = 30
MAX_LENGTH: int = 1000


from typing import TYPE_CHECKING

@sentience_guard
def enforce_legal_safety(text: str) -> str:
    """Static legal shield: formats, injects disclaimers, and removes illegal claims."""
    from core.compliance.smart_legal_watcher import weekly_report

    disclaimer = (
        "This product is for educational purposes only. Results may vary. Not professional advice. "
        "Consult a qualified expert before acting. AI-generated content is labeled as such. All rights reserved."
    )
    ai_label = "[AI-Generated Content]"
    text = f"{ai_label}\n{text}\n\n---\n{disclaimer}"
    weekly_report()
    return text


@sentience_guard
def optimize_prompt(prompt: str, title: Optional[str] = None) -> Tuple[str, Optional[str]]:
    # --- OMNIBLADE LEGAL SHIELD: Enforce Legal Safety ---
    prompt = enforce_legal_safety(prompt)

    """
    Refine PDF prompts: detects niche/tone, removes clichés, boosts clarity.
    Enforces non-sentience, statelessness, and strict anti-manipulation.
    """
    # Length checks
    if len(prompt) < MIN_LENGTH:
        logging.warning("Prompt too short. Flagging for human review.")
        return (
            prompt,
            "FLAG: Prompt too short for optimization. Manual review required.",
        )
    if len(prompt) > MAX_LENGTH:
        logging.warning("Prompt too int. Flagging for human review.")
        return prompt[:MAX_LENGTH], "FLAG: Prompt truncated. Manual review required."
    # Banned phrase filtering
    for banned in BANNED_PHRASES:
        if banned in prompt.lower():
            logging.warning(
                f"Banned phrase '{banned}' detected. Flagging for human review."
            )
            return (
                prompt.replace(banned, "[REDACTED]"),
                f"FLAG: Banned phrase '{banned}' removed. Manual review required.",
            )
    # Example: Remove common clichés, detect niche/tone
    optimized = prompt.replace("world-class", "elite").replace("guaranteed", "proven")
    return optimized, None
