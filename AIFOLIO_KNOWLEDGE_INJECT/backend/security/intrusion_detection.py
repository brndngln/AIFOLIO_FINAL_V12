"""
AIFOLIO Intrusion Detection & Anti-Bot
Static, deterministic, SAFE AI-compliant challenge-response, Captcha, and canary token logic.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_CANARY_TOKENS = ["canary-1234", "canary-5678"]
STATIC_CHALLENGE_QUESTIONS = ["What is 2+2?", "Type the word SAFE"]


def is_canary_triggered(token: str) -> bool:
    triggered = token in STATIC_CANARY_TOKENS
    logger.info(f"Canary token check: {token} triggered={triggered}")
    return triggered


def challenge_response(answer: str) -> bool:
    allowed = answer.strip().lower() in ["4", "safe"]
    logger.info(f"Challenge response: {answer} allowed={allowed}")
    return allowed
