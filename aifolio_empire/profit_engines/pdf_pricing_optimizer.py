"""
AIFOLIO PDF Pricing Optimizer
Static, deterministic, SAFE AI-compliant pricing logic for PDFs, including split-testing and conversion tracking.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_PRICES = [19, 29, 49, 99, 199, 499]
STATIC_SPLIT_GROUPS = ['A', 'B']
STATIC_CONVERSION_RATES = {'A': 0.12, 'B': 0.15}


def assign_split_group(user_id: str) -> str:
    """Deterministically assign user to split group."""
    group = STATIC_SPLIT_GROUPS[0] if int(user_id[-1], 16) % 2 == 0 else STATIC_SPLIT_GROUPS[1]
    logger.info(f"User {user_id} assigned to group {group}")
    return group

def get_price_for_group(group: str) -> int:
    """Return static price for split group."""
    idx = 0 if group == 'A' else 1
    price = STATIC_PRICES[idx]
    logger.info(f"Price for group {group}: {price}")
    return price

def get_conversion_rate(group: str) -> float:
    """Return static conversion rate for split group."""
    rate = STATIC_CONVERSION_RATES[group]
    logger.info(f"Conversion rate for group {group}: {rate}")
    return rate
