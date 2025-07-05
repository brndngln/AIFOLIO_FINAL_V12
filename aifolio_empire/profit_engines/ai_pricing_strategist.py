"""
AIFOLIO™ AI Pricing Strategist
Adaptive price testing, demand-based promotions, and bundle logic for PDFs. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_PRICING_GROUPS = ["Standard", "Premium", "VIP", "Bundle"]
STATIC_PROMOTIONS = ["Launch Discount", "Holiday Sale", "Flash Deal"]


def get_adaptive_price(pdf_id, base_price, demand_factor=1.0, group="Standard"):
    """Returns a static, deterministic price for a PDF based on group and demand."""
    if group not in STATIC_PRICING_GROUPS:
        group = "Standard"
    promo = STATIC_PROMOTIONS[0] if demand_factor > 1.2 else None
    price = round(base_price * demand_factor, 2)
    logging.info(
        f"AI Pricing Strategist: PDF {pdf_id}, Group: {group}, Price: {price}, Promo: {promo}"
    )
    return {"pdf_id": pdf_id, "group": group, "price": price, "promo": promo}
