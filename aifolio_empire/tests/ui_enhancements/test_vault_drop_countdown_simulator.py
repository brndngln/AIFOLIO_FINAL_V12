"""
Unit tests for the VaultDropCountdownSimulator.
"""

import unittest
import sys
import os
from datetime import datetime, timezone, timedelta
import importlib
from unittest.mock import Mock

# Adjust path to import module from parent directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(
    os.path.dirname(current_dir)
)  # This should be aifolio_empire
src_dir = os.path.join(parent_dir, "ui_enhancements")
sys.path.insert(0, parent_dir)  # Add aifolio_empire to path to find ui_enhancements

from ui_enhancements.vault_drop_countdown_simulator import VaultDropCountdownSimulator


class TestVaultDropCountdownSimulator(unittest.TestCase):
    """Test suite for the VaultDropCountdownSimulator."""

    def setUp(self) -> None:
        """Set up for each test."""
        self.simulator = VaultDropCountdownSimulator()
        self.test_vault_id = "vault_test_123"
        # Original datetime objects for potential direct use if needed
        self.test_target_datetime_future_obj = datetime.now(timezone.utc) + timedelta(
            days=5
        )
        self.test_target_datetime_past_obj = datetime.now(timezone.utc) - timedelta(
            days=5
        )
        # ISO strings formatted with 'Z' for passing to the simulator
        self.test_target_datetime_future_iso = (
            self.test_target_datetime_future_obj.isoformat().replace("+00:00", "Z")
        )
        self.test_target_datetime_past_iso = (
            self.test_target_datetime_past_obj.isoformat().replace("+00:00", "Z")
        )

    def test_simulator_initialization(self) -> None:
        """Test that the simulator can be initialized."""
        self.assertIsNotNone(self.simulator)

    def test_get_simulated_countdown_future_basic_structure(self) -> None:
        """Test the basic structure of the output for a future target."""
        result = self.simulator.get_simulated_countdown(
            self.test_target_datetime_future_iso, self.test_vault_id
        )
        self.assertIn("action_id_sim", result)
        self.assertTrue(
            result["action_id_sim"].startswith(f"countdown_{self.test_vault_id}_")
        )
        self.assertIn("vault_id_sim", result)
        self.assertEqual(result["vault_id_sim"], self.test_vault_id)
        self.assertIn("target_time_utc_sim", result)  # Renamed key
        self.assertEqual(
            result["target_time_utc_sim"], self.test_target_datetime_future_iso
        )
        self.assertIn("current_datetime_utc_sim", result)
        self.assertIn("details_sim", result)  # Changed from countdown_data_sim
        self.assertIn("display_text_sim", result)
        self.assertIn("status_message_sim", result)  # May be None
        self.assertIn("glitch_message_sim", result)  # May be None
        self.assertIn("anti_sentience_notes_sim", result)
        self.assertIsInstance(result["anti_sentience_notes_sim"], str)

    def test_get_simulated_countdown_past_basic_structure(self) -> None:
        """Test the basic structure of the output for a past target."""
        result = self.simulator.get_simulated_countdown(
            self.test_target_datetime_past_iso, self.test_vault_id
        )
        self.assertFalse(result["countdown_active_sim"])
        self.assertIn("details_sim", result)  # Check for details structure
        self.assertIn("display_text_sim", result)  # e.g., "DROP IS LIVE!"
        # For past events, status_message_sim is not explicitly set in the same way as future ones.
        # The primary indicator is countdown_active_sim = False and the display_text_sim.
        self.assertTrue(
            result["display_text_sim"] in ["DROP IS LIVE!", "EVENT ACTIVE!"]
        )

    def test_countdown_data_structure(self) -> None:
        """Test the structure within countdown_data_sim."""
        result = self.simulator.get_simulated_countdown(
            self.test_target_datetime_future_iso, self.test_vault_id
        )
        self.assertIn("details_sim", result)
        countdown_data = result["details_sim"]  # Changed from countdown_data_sim

        self.assertIn("days_sim", countdown_data)
        self.assertIn("hours_sim", countdown_data)
        self.assertIn("minutes_sim", countdown_data)
        self.assertIn("seconds_sim", countdown_data)
        self.assertIn("total_seconds_remaining_sim", countdown_data)
        self.assertIsInstance(countdown_data["days_sim"], int)
        self.assertIsInstance(countdown_data["hours_sim"], int)
        self.assertIsInstance(countdown_data["minutes_sim"], int)
        self.assertIsInstance(countdown_data["seconds_sim"], int)
        self.assertIsInstance(
            countdown_data["total_seconds_remaining_sim"], int
        )  # Should be int after casting in simulator
        # glitch_message_sim and status_message_sim are now top-level in the result for future events
        self.assertIn("glitch_message_sim", result)
        self.assertTrue(isinstance(result["glitch_message_sim"], (str, type(None))))
        self.assertIn("status_message_sim", result)
        self.assertTrue(isinstance(result["status_message_sim"], (str, type(None))))

    def test_anti_sentience_markers(self) -> None:
        """Test for the presence of _sim suffixes and anti_sentience_notes."""
        result = self.simulator.get_simulated_countdown(
            self.test_target_datetime_future_iso, self.test_vault_id
        )

        # Check some key fields for _sim suffix
        self.assertTrue(any("_sim" in key for key in result.keys()))
        if "details_sim" in result:  # details_sim contains the countdown numbers
            self.assertTrue(any("_sim" in key for key in result["details_sim"].keys()))
        if result.get("countdown_active_sim", False):
            self.assertGreater(len(result["anti_sentience_notes_sim"]), 0)
        # For past events, anti_sentience_notes_sim might not be present based on current simulator code

    def test_statelessness_action_id_uniqueness(self) -> None:
        """Test that action_id_sim is unique across calls (simple check for statelessness)."""
        result1 = self.simulator.get_simulated_countdown(
            self.test_target_datetime_future_iso, self.test_vault_id
        )
        result2 = self.simulator.get_simulated_countdown(
            self.test_target_datetime_future_iso, self.test_vault_id
        )
        self.assertNotEqual(result1["action_id_sim"], result2["action_id_sim"])

    def test_invalid_datetime_format(self) -> None:
        """Test behavior with an invalid datetime string."""
        invalid_dt_string = "not-a-datetime"
        result = self.simulator.get_simulated_countdown(
            invalid_dt_string, self.test_vault_id
        )
        self.assertIn("error_sim", result)
        self.assertEqual(
            result["error_sim"], "Invalid target datetime format provided."
        )
        self.assertEqual(result["raw_target_sim"], invalid_dt_string)
        self.assertFalse(result["countdown_active_sim"])
        self.assertEqual(
            result["vault_id_sim"], self.test_vault_id
        )  # Assuming vault_id is still correctly passed through in error cases

    def test_config_logger_fallback(self) -> None:
        """Test that the simulator runs with fallback config by directly patching the module's config."""
        simulator_module_name = "ui_enhancements.vault_drop_countdown_simulator"

        # Ensure the simulator module is loaded
        if simulator_module_name not in sys.modules:
            importlib.import_module(simulator_module_name)

        simulator_module = sys.modules[simulator_module_name]

        # Store the original config object from the simulator module
        original_module_config = getattr(simulator_module, "config", None)

        try:
            # Directly replace the 'config' in the simulator module with its own MockConfig
            # This assumes MockConfig is defined within vault_drop_countdown_simulator.py
            # which it is, inside the except ImportError block.
            if not hasattr(simulator_module, "config"):
                simulator_module.config = simulator_module.MockConfig()

            # Verify that the module is now using MockConfig
            self.assertEqual(
                simulator_module.config.__class__.__name__,
                "MockConfig",
                "Simulator module should be using MockConfig.",
            )

            # Initialize the simulator. It should now use the MockConfig we just set.
            temp_simulator = simulator_module.VaultDropCountdownSimulator()
            result = temp_simulator.get_simulated_countdown(
                self.test_target_datetime_future_iso, self.test_vault_id
            )
            self.assertIn(
                "action_id_sim", result
            )  # Basic check that it produced output

            # Verify a value from MockConfig to be sure
            self.assertEqual(
                simulator_module.config.SIM_COUNTDOWN_MAX_JITTER_SECONDS, 5
            )

        finally:
            # Restore the original config object to the simulator module
            if original_module_config is not None:
                if not hasattr(simulator_module, "config"):
                    simulator_module.config = Mock()
                simulator_module.config = original_module_config
            elif hasattr(
                simulator_module, "config"
            ):  # If it was set by us but wasn't there before
                delattr(simulator_module, "config")

            # Optional: Reload the module to ensure it's in a clean state for other tests,
            # though direct restoration above should be sufficient if MockConfig isn't global.
            # importlib.reload(simulator_module)


if __name__ == "__main__":
    unittest.main()
