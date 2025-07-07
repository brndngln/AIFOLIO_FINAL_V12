"""
AIFOLIO™ Loyalty Loop AI
Recognizes top buyers and auto-offers upsells or gifts. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_TOP_BUYERS = ["alice@example.com", "bob@example.com"]
STATIC_GIFTS = ["Free Upgrade", "Bonus PDF"]


from typing import Dict, Optional

def get_loyalty_offer(user_email: str) -> Optional[Dict[str, str]]:
    if user_email in STATIC_TOP_BUYERS:
        gift = STATIC_GIFTS[0]
        logging.info(f"Loyalty Loop AI: User {user_email} recognized, Gift: {gift}")
        return {"user": user_email, "gift": gift}
    return None
