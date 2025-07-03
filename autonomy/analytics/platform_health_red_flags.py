"""
AIFOLIO SAFE AI Platform Health Red Flags Report
- Flags static anomalies in system health
"""
def platform_health_red_flags(health_metrics):
    # Expects: dict of metrics
    # Example: flag if any metric exceeds static threshold
    flags = {k: v for k, v in health_metrics.items() if v > 100}
    return {'red_flags': flags}
