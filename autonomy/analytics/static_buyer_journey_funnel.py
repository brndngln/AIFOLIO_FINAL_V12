"""
AIFOLIO SAFE AI Static Buyer Journey Funnel
- Tracks aggregate steps: View → Add to Cart → Purchase
- No personalization, no targeting, no optimization
"""


def buyer_journey_funnel(data):
    # Expects: {'views': int, 'add_to_cart': int, 'purchases': int}
    funnel = {
        "views": data.get("views", 0),
        "add_to_cart": data.get("add_to_cart", 0),
        "purchases": data.get("purchases", 0),
        "view_to_cart_rate": (data.get("add_to_cart", 0) / data.get("views", 1)) * 100
        if data.get("views", 0)
        else 0,
        "cart_to_purchase_rate": (data.get("purchases", 0) / data.get("add_to_cart", 1))
        * 100
        if data.get("add_to_cart", 0)
        else 0,
    }
    return funnel
