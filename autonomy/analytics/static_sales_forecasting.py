"""
AIFOLIO SAFE AI Static Sales Forecasting
- Calendar-based, no static logic, no learning
- Forecasts sales if current trend holds
"""


from typing import Dict

def static_sales_forecast(sales_by_month: Dict[str, float]) -> Dict[str, float]:
    """
    SAFE AI-compliant: Static sales forecast. Deterministic, owner-controlled, no adaptive logic.
    """
    if not sales_by_month:
        return {"forecast": 0.0}
    last_month = list(sorted(sales_by_month.keys()))[-1]
    forecast = sales_by_month[last_month]
    return {"next_month_forecast": forecast}
