"""
AIFOLIO SAFE AI Static Funnel Reports
- View → Add to Cart → Purchase (aggregate only)
"""


def static_funnel_report(funnel_data):
    # Expects: {'views': int, 'add_to_cart': int, 'purchases': int}
    return {
        "views": funnel_data.get("views", 0),
        "add_to_cart": funnel_data.get("add_to_cart", 0),
        "purchases": funnel_data.get("purchases", 0),
        "view_to_cart_rate": (
            funnel_data.get("add_to_cart", 0) / funnel_data.get("views", 1)
        )
        * 100
        if funnel_data.get("views", 0)
        else 0,
        "cart_to_purchase_rate": (
            funnel_data.get("purchases", 0) / funnel_data.get("add_to_cart", 1)
        )
        * 100
        if funnel_data.get("add_to_cart", 0)
        else 0,
    }
