import requests
import json
from pathlib import Path
from typing import List, Dict, Any

FEED_URLS: List[str] = [
    "https://www.iso.org/isoiec-27001-information-security.html",
    "https://www.nist.gov/topics/computer-security",
    # Add more external compliance sources as needed
]
FEED_CACHE: Path = Path(__file__).parent.parent / "logs" / "compliance_feeds.json"

# Deterministic, SAFE AI-compliant compliance feed fetcher
# No adaptive or sentient logic; static, explainable, OWNER-controlled


def fetch_compliance_feeds() -> List[Dict[str, Any]]:
    """
    SAFE AI-compliant: Static compliance feed fetcher. Deterministic, owner-controlled, no adaptive logic.
    """
    feeds: List[Dict[str, Any]] = []
    for url in FEED_URLS:
        try:
            # For demo, just fetch the page title or first 500 chars
            resp = requests.get(url, timeout=10)
            snippet = resp.text[:500]
            feeds.append({"url": url, "snippet": snippet})
        except Exception as e:
            feeds.append({"url": url, "error": str(e)})
    with open(FEED_CACHE, "w") as f:
        json.dump(feeds, f, indent=2)
    return feeds
