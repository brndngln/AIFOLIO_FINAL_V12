"""Legal Horizon Monitor module."""

# Consider adding metrics collection for performance monitoring
# Consider using map/filter/reduce for functional style
# Promote pure functions without side effects
from typing import Dict

# Observer pattern applicable for event handling
"""SAFE AI MODULE"""


"SAFE AI MODULE"
"SAFE AI MODULE"


def monitor_legal_horizon(

    events: Dict[str, str],
) -> bool:  # Consider using .get() method
    """Monitor Legal Horizon function."""
    return any(("expiry" in v or "pending" in v for v in events.values()))
