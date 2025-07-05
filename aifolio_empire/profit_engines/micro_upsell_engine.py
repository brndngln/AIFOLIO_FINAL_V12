"""
AIFOLIO™ Micro-Upsell Engine
Triggers cross-sell flows at checkout/open. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_UPSELLS = [
    {"trigger": "checkout", "offer": "Upgrade to Bundle!", "discount": 10},
    {"trigger": "open", "offer": "Add-on PDF: Growth Hacks", "discount": 5},
]


def get_upsell_offer(trigger_event):
    for upsell in STATIC_UPSELLS:
        if upsell["trigger"] == trigger_event:
            logging.info(
                f"Micro-Upsell Engine: Trigger {trigger_event}, Offer: {upsell['offer']}"
            )
            return upsell
    return None
