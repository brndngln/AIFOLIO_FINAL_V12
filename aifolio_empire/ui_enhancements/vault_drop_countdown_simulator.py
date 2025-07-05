"""
Vault Drop Countdown Simulator with strict anti-sentience measures.
This module simulates the logic for a real-time countdown to a vault drop or event.
It is stateless per operation, rule-based, and includes simulated imperfections.
"""

import random
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any


# Define MockConfig at module level
class MockConfig:
    SIM_COUNTDOWN_MAX_JITTER_SECONDS = 5  # Max seconds +/- for simulated inaccuracy
    SIM_COUNTDOWN_RECALCULATING_CHANCE = 0.02  # Chance to show 'recalculating' message
    SIM_COUNTDOWN_GLITCH_CHANCE = 0.005  # Chance of a minor display glitch message


# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print(
        "Warning: Could not import 'config' and 'logger' directly. Using basic logging."
    )
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    config = MockConfig()  # Instantiated from module-level class


class VaultDropCountdownSimulator:
    """Simulates vault drop countdown logic with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. All operations are conceptually stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("VaultDropCountdownSimulator initialized. Operations stateless.")

    def get_simulated_countdown(
        self, target_datetime_utc_iso_original: str, vault_id_sim: str
    ) -> Dict[str, Any]:
        """Simulates calculating and formatting a countdown to a target datetime.
        Args:
            target_datetime_utc_iso: The target datetime in ISO format (UTC).
                                     Example: "2024-12-31T23:59:59Z"
            vault_id_sim: A simulated ID for the vault or event being counted down to.
        Returns:
            A dictionary containing countdown details or an error message.
        """
        action_id = f"countdown_{vault_id_sim}_{uuid.uuid4().hex[:8]}"
        current_time_utc = datetime.now(timezone.utc)
        status_message_sim = None
        glitch_message_sim = None  # Initialize glitch message
        anti_sentience_notes = []
        target_datetime_utc_iso = target_datetime_utc_iso_original  # Work with a copy

        try:
            # Ensure the input string ends with 'Z' for UTC and parse it
            if not target_datetime_utc_iso.endswith("Z"):
                target_datetime_utc_iso += "Z"
            target_time_utc = datetime.fromisoformat(
                target_datetime_utc_iso.replace("Z", "+00:00")
            )
            if target_time_utc.tzinfo is None:
                target_time_utc = target_time_utc.replace(
                    tzinfo=timezone.utc
                )  # Ensure tz aware
        except ValueError as e:
            logger.error(
                f"Invalid target_datetime_utc_iso format: {target_datetime_utc_iso_original}. Error: {e}"
            )  # Log original
            return {
                "action_id_sim": action_id,
                "vault_id_sim": vault_id_sim,
                "error_sim": "Invalid target datetime format provided.",
                "raw_target_sim": target_datetime_utc_iso_original,  # Return original
                "countdown_active_sim": False,
            }

        time_remaining = target_time_utc - current_time_utc

        # Anti-sentience: Introduce simulated jitter/inaccuracy
        # Patch: Use getattr for config fields for Pydantic compatibility
        max_jitter = getattr(config, "SIM_COUNTDOWN_MAX_JITTER_SECONDS", 5)
        jitter_seconds = random.randint(-max_jitter, max_jitter)
        time_remaining += timedelta(seconds=jitter_seconds)
        if jitter_seconds != 0:
            anti_sentience_notes.append(f"Time jittered by {jitter_seconds}s.")

        if time_remaining.total_seconds() <= 0:
            return {
                "action_id_sim": action_id,
                "vault_id_sim": vault_id_sim,
                "countdown_active_sim": False,
                "display_text_sim": "DROP IS LIVE!"
                if random.random() > 0.1
                else "EVENT ACTIVE!",
                "details_sim": {
                    "days_sim": 0,
                    "hours_sim": 0,
                    "minutes_sim": 0,
                    "seconds_sim": 0,
                    "total_seconds_remaining_sim": 0,
                },
                "target_time_utc_sim": target_datetime_utc_iso,
                "jitter_applied_seconds_sim": jitter_seconds,
                "glitch_message_sim": None,  # No glitch if drop is live
                "status_message_sim": None,  # No specific status if drop is live
                "anti_sentience_notes_sim": "; ".join(anti_sentience_notes)
                if anti_sentience_notes
                else "Standard simulation.",
            }

        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        display_text = f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

        # Anti-sentience: Simulate recalculating or glitch messages
        recalc_chance = getattr(config, "SIM_COUNTDOWN_RECALCULATING_CHANCE", 0.02)
        glitch_chance = getattr(config, "SIM_COUNTDOWN_GLITCH_CHANCE", 0.005)
        if random.random() < recalc_chance:
            status_message_sim = "Recalculating... (simulated)"
            display_text = "--d --h --m --s"  # Simulate placeholder during recalc
            logger.info(f"Simulated 'recalculating' state for countdown {action_id}")
            anti_sentience_notes.append("Simulated recalculation event.")
        elif random.random() < glitch_chance:
            glitch_message_sim = "Display sync error... retrying (simulated_glitch)"
            # Corrupt one of the display values slightly
            if random.random() < 0.5 and seconds > 5:
                seconds_glitched = max(0, seconds - random.randint(1, 5))
                display_text = f"{days:02d}d {hours:02d}h {minutes:02d}m {seconds_glitched:02d}s (glitch)"
            else:
                display_text = (
                    f"{days:02d}d {hours:02d}h ?{minutes:02d}?m {seconds:02d}s"
                )
            logger.warning(f"Simulated display glitch for countdown {action_id}")
            anti_sentience_notes.append("Simulated display glitch event.")

        return {
            "action_id_sim": action_id,
            "vault_id_sim": vault_id_sim,
            "countdown_active_sim": True,
            "display_text_sim": display_text,
            "details_sim": {
                "days_sim": days,
                "hours_sim": hours,
                "minutes_sim": minutes,
                "seconds_sim": seconds,
                "total_seconds_remaining_sim": int(time_remaining.total_seconds())
                if time_remaining.total_seconds() > 0
                else 0,
            },
            "target_time_utc_sim": target_datetime_utc_iso,
            "status_message_sim": status_message_sim,
            "glitch_message_sim": glitch_message_sim,
            "jitter_applied_seconds_sim": jitter_seconds,
            "current_datetime_utc_sim": current_time_utc.isoformat().replace(
                "+00:00", "Z"
            ),
            "anti_sentience_notes_sim": "; ".join(anti_sentience_notes)
            if anti_sentience_notes
            else "Standard simulation.",
        }


# Example Usage:
if __name__ == "__main__":
    import json
    import time

    logger.info("--- Running VaultDropCountdownSimulator Example ---")
    simulator = VaultDropCountdownSimulator()

    # Simulate a drop in 1 day, 2 hours, 30 minutes
    future_time = datetime.now(timezone.utc) + timedelta(
        days=1, hours=2, minutes=30, seconds=15
    )
    target_iso = future_time.isoformat().replace("+00:00", "Z")

    print(f"\n⏳ Countdown to: {target_iso} (Vault: 'alpha_launch') ⏳")
    countdown_data = simulator.get_simulated_countdown(target_iso, "alpha_launch")
    print(json.dumps(countdown_data, indent=2))

    # Simulate a drop that just passed
    past_time = datetime.now(timezone.utc) - timedelta(minutes=5)
    target_past_iso = past_time.isoformat().replace("+00:00", "Z")
    print(
        f"\n⏳ Countdown to: {target_past_iso} (Vault: 'beta_drop' - already passed) ⏳"
    )
    countdown_past = simulator.get_simulated_countdown(target_past_iso, "beta_drop")
    print(json.dumps(countdown_past, indent=2))

    # Simulate with invalid format
    print("\n⏳ Countdown with invalid format (Vault: 'gamma_error') ⏳")
    countdown_error = simulator.get_simulated_countdown("NOT_A_DATETIME", "gamma_error")
    print(json.dumps(countdown_error, indent=2))

    # Simulate multiple calls to see jitter/recalc chances
    print("\n⏳ Simulating multiple calls for 'delta_promo' (target in 10 seconds) ⏳")
    short_future_time = datetime.now(timezone.utc) + timedelta(seconds=10)
    short_target_iso = short_future_time.isoformat().replace("+00:00", "Z")
    for i in range(5):
        print(f"  Call {i+1}:")
        cd_short = simulator.get_simulated_countdown(
            short_target_iso, f"delta_promo_run_{i}"
        )
        print(
            f"    Display: {cd_short.get('display_text_sim')}, Status: {cd_short.get('status_message_sim')}, Jitter: {cd_short.get('jitter_applied_seconds_sim')}s"
        )
        if i < 4:
            time.sleep(0.5)  # Small delay between simulated calls

    logger.info("--- VaultDropCountdownSimulator Example Finished ---")
