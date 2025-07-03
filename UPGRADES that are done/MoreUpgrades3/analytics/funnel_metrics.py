import json
import statistics

def get_funnel_metrics():
    try:
        with open("analytics/engagement_log.json", "r") as f:
            logs = [json.loads(line) for line in f]
    except FileNotFoundError:
        return {}

    metrics = {
        "downloads": 0,
        "purchases": 0,
        "upsells": 0,
        "conversion_rate": 0.0,
        "top_products": {},
        "drop_off_points": {}
    }

    for log in logs:
        action = log["action"]
        product = log["product_id"]
        metrics["top_products"].setdefault(product, {"downloads": 0, "purchases": 0, "upsells": 0})
        if action == "download":
            metrics["downloads"] += 1
            metrics["top_products"][product]["downloads"] += 1
        elif action == "purchase":
            metrics["purchases"] += 1
            metrics["top_products"][product]["purchases"] += 1
        elif action == "upsell":
            metrics["upsells"] += 1
            metrics["top_products"][product]["upsells"] += 1
        elif action == "drop_off":
            metrics["drop_off_points"].setdefault(product, 0)
            metrics["drop_off_points"][product] += 1

    try:
        metrics["conversion_rate"] = round((metrics["purchases"] / metrics["downloads"]) * 100, 2)
    except ZeroDivisionError:
        metrics["conversion_rate"] = 0.0

    return metrics