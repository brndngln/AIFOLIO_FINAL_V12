"""
AIFOLIO SAFE AI Revenue Milestone Tracker (static, non-sentient)
- Logs when revenue thresholds are hit
- All actions logged to analytics_log.json
"""
import json
import os
from datetime import datetime

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "analytics_log.json")
)

MILESTONES = [1000, 5000, 10000, 50000, 100000]


def check_milestones(total_revenue):
    hit = [m for m in MILESTONES if total_revenue >= m]
    if hit:
        with open(LOG_PATH, "a") as f:
            f.write(
                json.dumps(
                    {
                        "action": "milestone_hit",
                        "milestones": hit,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                + "\n"
            )
    return hit
