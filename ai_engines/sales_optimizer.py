"""
Sales Optimization Engine (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
import logging

BANNED_SALES_PHRASES = [
    "guaranteed",
    "secret",
    "get rich",
    "overnight",
    "never fail",
    "loophole",
    "limited time",
    "exclusive access",
]


@sentience_guard
def suggest_sales_improvements(product_text):
    """
    Analyze product for keyword/title/CTA/upsell improvements.
    Enforces non-sentience, statelessness, anti-manipulation, and transparency.
    """
    suggestions = []
    for banned in BANNED_SALES_PHRASES:
        if banned in product_text.lower():
            logging.warning(
                f"Banned sales phrase '{banned}' detected. Flagging for human review."
            )
            suggestions.append(
                f"FLAG: Banned phrase '{banned}' found. Manual review required."
            )
    if not suggestions:
        suggestions = [
            "Rewrite CTA for clarity and transparency",
            "Add factual upsell section",
        ]
    return suggestions
