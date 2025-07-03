"""
SAFE AI Static Module: Geo-Aware Latency Optimization (Static)
- Logs static, preconfigured latency checks per region
- No dynamic or learning behavior
"""
import logging
from datetime import datetime as statictime

LOG_PATH = "../../distribution/legal_exports/geo_latency_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

REGIONS = ["us-east-1", "eu-west-1", "ap-southeast-1"]

PRECONFIGURED_LATENCIES = {
    "us-east-1": 45,
    "eu-west-1": 60,
    "ap-southeast-1": 80
}


def log_latency(region, latency, triggered_by):
    timestamp = statictime.utcnow().isoformat()
    event = f"[{timestamp}] LATENCY: {region} | Latency: {latency}ms | Triggered by: {triggered_by}"
    logging.info(event)
    return event


def run_geo_latency_check(triggered_by):
    for region, latency in PRECONFIGURED_LATENCIES.items():
        log_latency(region, latency, triggered_by)
    return "Geo-latency check logged."
