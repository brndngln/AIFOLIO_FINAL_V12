"""
AIFOLIO SAFE AI Seasonal Sales Pattern Report
- Static, aggregate, flags months with high/low sales
"""


from typing import Any

def seasonal_sales_pattern(sales_by_month: Any) -> Any:
    # Expects: {'YYYY-MM': value, ...}
    if not sales_by_month:
        return {"seasonal_pattern": []}
    import statistics

    values = list(sales_by_month.values())
    avg = statistics.mean(values)
    pattern = [{"month": k, "above_avg": v > avg} for k, v in sales_by_month.items()]
    return {"seasonal_pattern": pattern}
