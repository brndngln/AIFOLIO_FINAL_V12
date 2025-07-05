"""
SAFE AI Static Module: Buyer Sentiment Explorer
- Explores static buyer sentiment data (table-driven, no static logic)
- Logs all explorations for admin review
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/buyer_sentiment_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SENTIMENT_TABLE = {"positive": 120, "neutral": 65, "negative": 15}


def explore_sentiment(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] BUYER SENTIMENT: {SENTIMENT_TABLE} | Triggered by: {triggered_by}"
    logging.info(event)
    return SENTIMENT_TABLE
