"""
AIFOLIO Rate Limiting & DoS Protection
Static, deterministic, SAFE AI-compliant rate limiter and audit logger.
"""
import logging
import time
from collections import defaultdict
logger = logging.getLogger(__name__)

STATIC_LIMITS = {'/api/vault': 10, '/api/admin': 5}  # max requests per minute

class StaticRateLimiter:
    _last_reset = time.time()
    _counters = defaultdict(int)

    @classmethod
    def check(cls, endpoint: str, user_id: str) -> bool:
        now = time.time()
        if now - cls._last_reset > 60:
            cls._last_reset = now
            cls._counters.clear()
        key = f"{endpoint}:{user_id}"
        cls._counters[key] += 1
        allowed = cls._counters[key] <= STATIC_LIMITS.get(endpoint, 10)
        logger.info(f"Rate limit check for {key}: {allowed}")
        return allowed
