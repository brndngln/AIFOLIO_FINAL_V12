"""
SAFE AI Static Module: Autonomous Load Forecasting (Static)
- Logs static, preconfigured load forecasts for audit
- No adaptive, learning, or emergent behavior
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/load_forecasting_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

PRECONFIGURED_FORECASTS = {
    "us-east-1": [100, 120, 110],
    "eu-west-1": [80, 90, 95],
    "ap-southeast-1": [60, 70, 65]
}


def log_forecast(region, forecast, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] LOAD FORECAST: {region} | Forecast: {forecast} | Triggered by: {triggered_by}"
    logging.info(event)
    return event


def run_static_forecast(triggered_by):
    for region, values in PRECONFIGURED_FORECASTS.items():
        forecast = sum(values) // len(values)
        log_forecast(region, forecast, triggered_by)
    return "Static load forecast logged."
