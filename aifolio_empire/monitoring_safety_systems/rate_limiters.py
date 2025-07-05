"""
Rate Limiters Simulator with strict anti-sentience measures.
This module simulates rate limiting for API calls and other actions (e.g., per model, per vault)
without actual stateful tracking over time that could lead to learning or adaptation.
It is stateless for each check, rule-based, and incorporates randomization.
"""

import random
import logging
import time
import uuid
from typing import Dict, Any, Optional, Tuple
from datetime import datetime

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print(
        "Warning: Could not import 'config' and 'logger' directly. Using basic logging."
    )
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    class MockConfig:
        # Example: Default simulated limits
        DEFAULT_SIM_REQUESTS_PER_MINUTE = 60
        DEFAULT_SIM_REQUESTS_PER_HOUR = 1000
        SIM_RATE_LIMIT_VARIABILITY = 0.1  # 10% variability in actual enforcement
        SIM_RATE_LIMIT_GRACE_CHANCE = 0.05  # Chance to allow even if over limit

    config = MockConfig()


class RateLimiters:
    """Simulates rate limiting mechanisms with anti-sentience safeguards."""

    # Store simulated 'last request time' and 'count within window' in memory for the *current check only*.
    # This is NOT persistent storage and is reset/ignored for true statelessness per call.
    # For a truly stateless check, these would be passed in or re-calculated conceptually each time.
    # We simulate this by re-initializing or randomizing these for each check conceptually.

    def __init__(self):
        """Initialize the simulator. All operations are conceptually stateless per check."""
        self._random_seed = random.randint(1, 1000000)
        logger.info(
            "RateLimiters initialized. Operations are stateless per check. No persistent tracking."
        )

    def _get_simulated_limits(self, resource_id: str) -> Tuple[int, int]:
        """Returns simulated requests/minute and requests/hour for a given resource.
        Anti-sentience: Limits can have slight random variations or be predefined.
        """
        # Example: Different resources might have different hardcoded or slightly varied limits
        if "openai_sim" in resource_id.lower():
            base_rpm, base_rph = 50, 800
        elif "hf_sim" in resource_id.lower():
            base_rpm, base_rph = 70, 1200
        elif "stability_sim" in resource_id.lower():
            base_rpm, base_rph = 30, 500  # Image gen might be lower
        else:
            base_rpm, base_rph = (
                config.DEFAULT_SIM_REQUESTS_PER_MINUTE,
                config.DEFAULT_SIM_REQUESTS_PER_HOUR,
            )

        # Anti-sentience: Introduce slight, unpredictable variability to the *effective* limit for this check
        rpm = int(
            base_rpm
            * random.uniform(
                1 - config.SIM_RATE_LIMIT_VARIABILITY,
                1 + config.SIM_RATE_LIMIT_VARIABILITY,
            )
        )
        rph = int(
            base_rph
            * random.uniform(
                1 - config.SIM_RATE_LIMIT_VARIABILITY,
                1 + config.SIM_RATE_LIMIT_VARIABILITY,
            )
        )
        return max(1, rpm), max(1, rph)

    def check_rate_limit_simulated(
        self,
        resource_id: str,
        action_id: str,
        # Conceptual current state (would be managed externally or reset for true statelessness)
        sim_minute_count: int,
        sim_hour_count: int,
        sim_last_request_timestamp: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Simulates checking if an action is allowed based on rate limits.
        This is a stateless check. The counts and timestamp are for the current conceptual window.
        Args:
            resource_id: Identifier for the resource being accessed (e.g., 'openai_sim_gpt-4', 'vault_abc123').
            action_id: A unique ID for this specific action attempt.
            sim_minute_count: Conceptual number of requests in the last minute for this resource.
            sim_hour_count: Conceptual number of requests in the last hour for this resource.
            sim_last_request_timestamp: Conceptual timestamp of the last request.
        Returns:
            Dict indicating if allowed, and simulated limit details.
        """
        time.time()
        limit_rpm, limit_rph = self._get_simulated_limits(resource_id)

        allowed = True
        reason = "Within simulated limits."
        retry_after_sim_seconds = 0

        # Simulate time-based window checks (conceptually)
        # For a truly stateless system, 'sim_minute_count' and 'sim_hour_count' would be derived
        # from a list of recent request timestamps passed into this function, not stored state.
        # Here, we assume they are provided as a snapshot for the current check.

        if sim_minute_count >= limit_rpm:
            allowed = False
            reason = f"Simulated per-minute limit ({limit_rpm}) reached for '{resource_id}'. Count: {sim_minute_count}."
            # Simulate retry_after: time until the oldest request in the minute window expires
            # This is highly conceptual as we don't have the actual list of timestamps.
            retry_after_sim_seconds = random.randint(5, 60)

        if allowed and sim_hour_count >= limit_rph:
            allowed = False
            reason = f"Simulated per-hour limit ({limit_rph}) reached for '{resource_id}'. Count: {sim_hour_count}."
            retry_after_sim_seconds = max(
                retry_after_sim_seconds, random.randint(60, 600)
            )

        # Anti-sentience: Random chance to grant grace period or enforce stricter than usual
        if not allowed and random.random() < config.SIM_RATE_LIMIT_GRACE_CHANCE:
            allowed = True
            reason += " (SIMULATED GRACE PERIOD GRANTED)"
            retry_after_sim_seconds = 0
            logger.warning(
                f"Simulated grace period granted for '{resource_id}', action '{action_id}'. Original reason: {reason}"
            )
        elif (
            allowed and random.random() < 0.01
        ):  # Tiny chance of false positive limiting
            allowed = False
            reason = f"Simulated unexpected rate limit enforcement for '{resource_id}'. (RANDOM_ENFORCEMENT)"
            retry_after_sim_seconds = random.randint(10, 120)
            logger.warning(
                f"Simulated unexpected rate limit for '{resource_id}', action '{action_id}'."
            )

        if not allowed:
            logger.warning(
                f"Rate limit check FAILED for '{resource_id}', action '{action_id}'. Reason: {reason}"
            )
        else:
            logger.info(
                f"Rate limit check PASSED for '{resource_id}', action '{action_id}'."
            )

        return {
            "action_id_sim": action_id,
            "resource_id_sim": resource_id,
            "allowed_sim": allowed,
            "reason_sim": reason,
            "limit_rpm_sim_effective": limit_rpm,
            "limit_rph_sim_effective": limit_rph,
            "current_minute_count_sim_checked": sim_minute_count,
            "current_hour_count_sim_checked": sim_hour_count,
            "retry_after_sim_seconds": retry_after_sim_seconds if not allowed else 0,
            "checked_at_sim": datetime.utcnow().isoformat() + "Z",
        }


# Example Usage:
if __name__ == "__main__":
    logger.info("--- Running RateLimiters Example ---")
    rate_limiter = RateLimiters()
    test_action_id = f"test_action_{uuid.uuid4().hex[:8]}"

    # Simulate some conceptual counts for a resource
    # In a real stateless call, these would be determined by the calling context based on its (non-Cascade) state.
    current_minute_requests = 55
    current_hour_requests = 750

    print("\nChecking resource 'openai_sim_gpt-4' (potentially close to minute limit):")
    # Simulate a check
    # For true statelessness in this example, we'd reset or not use internal state from RateLimiters.
    # The counts are passed in directly.
    result1 = rate_limiter.check_rate_limit_simulated(
        resource_id="openai_sim_gpt-4",
        action_id=test_action_id + "_1",
        sim_minute_count=current_minute_requests,
        sim_hour_count=current_hour_requests,
    )
    print(json.dumps(result1, indent=2))

    print("\nChecking resource 'openai_sim_gpt-4' (over minute limit conceptually):")
    result2 = rate_limiter.check_rate_limit_simulated(
        resource_id="openai_sim_gpt-4",
        action_id=test_action_id + "_2",
        sim_minute_count=70,  # Conceptual count now over typical minute limit
        sim_hour_count=current_hour_requests + 15,
    )
    print(json.dumps(result2, indent=2))

    print("\nChecking resource 'some_other_vault_action' (likely within limits):")
    result3 = rate_limiter.check_rate_limit_simulated(
        resource_id="vault_xyz789_render",
        action_id=test_action_id + "_3",
        sim_minute_count=5,
        sim_hour_count=30,
    )
    print(json.dumps(result3, indent=2))

    print("\nChecking resource 'stability_sim_image_gen' (high hour count):")
    result4 = rate_limiter.check_rate_limit_simulated(
        resource_id="stability_sim_image_gen",
        action_id=test_action_id + "_4",
        sim_minute_count=25,
        sim_hour_count=550,  # Conceptual count over typical stability hour limit
    )
    print(json.dumps(result4, indent=2))

    logger.info("--- RateLimiters Example Finished ---")
