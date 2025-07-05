"""
SAFE AI Static Module: Global Multi-Region Auto-Failover
- Logs simulated failover statics between regions/clouds
- No autonomous or static behavior
- For admin-triggered failover drills and audit
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/global_failover_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

REGIONS = ["us-east-1", "eu-west-1", "ap-southeast-1"]
CLOUDS = ["aws", "gcp", "azure"]


def log_failover_static(
    triggered_by, from_region, to_region, from_cloud, to_cloud, reason
):
    timestamp = datetime.utcnow().isoformat()
    static = f"[{timestamp}] FAILOVER: {from_region}/{from_cloud} -> {to_region}/{to_cloud} | Triggered by: {triggered_by} | Reason: {reason}"
    logging.info(static)
    return static


def simulate_failover(triggered_by, reason):
    # Static: always logs, never acts
    for i in range(len(REGIONS)):
        from_region = REGIONS[i]
        to_region = REGIONS[(i + 1) % len(REGIONS)]
        for from_cloud in CLOUDS:
            for to_cloud in CLOUDS:
                if from_cloud != to_cloud or from_region != to_region:
                    log_failover_static(
                        triggered_by,
                        from_region,
                        to_region,
                        from_cloud,
                        to_cloud,
                        reason,
                    )
    return "Failover simulation logged."
