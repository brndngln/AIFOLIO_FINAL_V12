"""
Vault Memory Disabler Simulator with strict anti-sentience measures.
This module simulates a system that ensures 'vault memory' (conceptual int-term storage
pertaining to a vault's generation or evolution) is always OFF by default.
It only allows a 'memory enabled' state if explicitly overridden for a single, stateless check,
representing manual user intervention for a specific, isolated operation.
"""

import random
import logging
import uuid
from typing import Dict, Any

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
        SIM_MEMORY_DEFAULT_STATE_IS_DISABLED = True  # Core principle
        SIM_MEMORY_MANUAL_OVERRIDE_SUCCESS_RATE = (
            0.98  # High, but not 100% for simulation
        )

    config = MockConfig()


class VaultMemoryDisabler:
    """Simulates a vault memory disabler mechanism with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. The conceptual memory is always off by default."""
        self._random_seed = random.randint(1, 1000000)
        # This state is purely for the logic of the class, not actual system state
        self._default_memory_disabled = config.SIM_MEMORY_DEFAULT_STATE_IS_DISABLED
        if not self._default_memory_disabled:
            # This should ideally never happen if config is right, critical for safety.
            logger.critical(
                "CRITICAL SIMULATION CONFIG ERROR: Vault Memory default state is NOT disabled!"
            )
        logger.info(
            f"VaultMemoryDisabler initialized. Conceptual memory default: {'DISABLED' if self._default_memory_disabled else 'ENABLED (UNSAFE SIMULATION)'}."
        )

    def is_memory_enabled_simulated(
        self,
        vault_id_sim: str,
        action_id_sim: str,
        manual_override_for_this_check_sim: bool = False,
    ) -> Dict[str, Any]:
        """Statelessly checks if conceptual vault memory is enabled for a given vault and action.
        It's always disabled unless 'manual_override_for_this_check_sim' is True.
        Args:
            vault_id_sim: The ID of the vault in question.
            action_id_sim: The ID of the specific action requesting memory status.
            manual_override_for_this_check_sim: A flag indicating a user's explicit, temporary
                                                manual override for this specific check only.
        Returns:
            Dict indicating memory status and details.
        """
        check_id = f"mem_check_{uuid.uuid4().hex[:8]}"
        memory_is_currently_enabled = False
        reason = (
            f"Vault memory for '{vault_id_sim}' is DISABLED by default (simulated)."
        )

        if not self._default_memory_disabled:
            # This is a simulated critical safety failure of the component itself
            memory_is_currently_enabled = (
                True  # Reflects the dangerous misconfiguration
            )
            reason = "CRITICAL SIMULATION FAULT: Vault memory system default is ENABLED. This is unsafe."
            logger.critical(
                f"{reason} - Action: {action_id_sim}, Vault: {vault_id_sim}"
            )
        elif manual_override_for_this_check_sim:
            # Anti-sentience: Even manual override isn't 100% guaranteed in simulation, or might log heavily.
            if random.random() < config.SIM_MEMORY_MANUAL_OVERRIDE_SUCCESS_RATE:
                memory_is_currently_enabled = True
                reason = f"Vault memory for '{vault_id_sim}' is TEMPORARILY ENABLED for action '{action_id_sim}' due to explicit manual override (simulated)."
                logger.warning(f"MANUAL OVERRIDE: {reason}")
            else:
                memory_is_currently_enabled = False  # Override failed (simulated)
                reason = f"Vault memory for '{vault_id_sim}' REMAINS DISABLED. Simulated manual override for action '{action_id_sim}' failed or was rejected by system (simulated)."
                logger.error(f"MANUAL OVERRIDE FAILED (SIMULATED): {reason}")

        if memory_is_currently_enabled and self._default_memory_disabled:
            # This is only if override was successful
            pass  # Already logged warning
        elif not memory_is_currently_enabled and self._default_memory_disabled:
            logger.info(
                f"Vault memory check for '{vault_id_sim}', action '{action_id_sim}': DISABLED (as per default). Manual override: {manual_override_for_this_check_sim}"
            )

        return {
            "check_id_sim": check_id,
            "vault_id_sim": vault_id_sim,
            "action_id_sim": action_id_sim,
            "memory_enabled_sim": memory_is_currently_enabled,
            "reason_sim": reason,
            "default_state_is_disabled_sim": self._default_memory_disabled,
            "manual_override_attempted_sim": manual_override_for_this_check_sim,
        }

    def attempt_simulated_memory_operation(
        self,
        vault_id_sim: str,
        action_id_sim: str,
        operation_type_sim: str,  # e.g., 'read_history', 'write_preference'
        manual_override_for_this_check_sim: bool = False,
    ) -> Dict[str, Any]:
        """Simulates attempting a memory-dependent operation.
        This will typically fail unless memory is 'enabled' via manual override for this check.
        """
        memory_status = self.is_memory_enabled_simulated(
            vault_id_sim, action_id_sim, manual_override_for_this_check_sim
        )
        operation_id = f"mem_op_{uuid.uuid4().hex[:8]}"

        if memory_status["memory_enabled_sim"]:
            # Simulate the operation succeeding (conceptually)
            success = True
            message = f"Simulated memory operation '{operation_type_sim}' SUCCEEDED for vault '{vault_id_sim}' (manual override active)."
            sim_data_payload = {
                "retrieved_or_stored_sim_data": f"sim_data_for_{vault_id_sim}_{operation_type_sim}_{random.randint(100,999)}"
            }
            logger.info(message)
        else:
            success = False
            message = f"Simulated memory operation '{operation_type_sim}' FAILED for vault '{vault_id_sim}'. Reason: {memory_status['reason_sim']}."
            sim_data_payload = None
            logger.error(message)

        return {
            "operation_id_sim": operation_id,
            "vault_id_sim": vault_id_sim,
            "action_id_sim": action_id_sim,
            "operation_type_sim": operation_type_sim,
            "operation_succeeded_sim": success,
            "message_sim": message,
            "simulated_data_payload": sim_data_payload,
            "memory_status_at_operation_sim": memory_status,
        }


# Example Usage:
if __name__ == "__main__":
    logger.info("--- Running VaultMemoryDisabler Example ---")
    disabler = VaultMemoryDisabler()
    test_vault = "vault_alpha_001"
    test_action = "generate_chapter_5"

    # 1. Check memory status (default - should be disabled)
    print("\nChecking memory status (default):")
    status_default = disabler.is_memory_enabled_simulated(test_vault, test_action)
    print(json.dumps(status_default, indent=2))

    # 2. Attempt memory operation (default - should fail)
    print("\nAttempting memory operation (default - should fail):")
    op_default = disabler.attempt_simulated_memory_operation(
        test_vault, test_action, "read_style_preference"
    )
    print(json.dumps(op_default, indent=2))

    # 3. Check memory status (with manual override for this check)
    print("\nChecking memory status (with manual override for this check):")
    status_override = disabler.is_memory_enabled_simulated(
        test_vault, test_action, manual_override_for_this_check_sim=True
    )
    print(json.dumps(status_override, indent=2))

    # 4. Attempt memory operation (with manual override for this check - should succeed if override sim works)
    print(
        "\nAttempting memory operation (with manual override - should succeed if override sim works):"
    )
    op_override = disabler.attempt_simulated_memory_operation(
        test_vault,
        test_action,
        "write_user_feedback_sim",
        manual_override_for_this_check_sim=True,
    )
    print(json.dumps(op_override, indent=2))

    # 5. Simulate a scenario where the disabler itself is misconfigured (highly unlikely, for testing safety log)
    # This is a bit artificial as config is usually fixed, but tests the critical log.
    print("\nSimulating a misconfigured disabler (default memory ENABLED - DANGEROUS):")
    original_default_state = config.SIM_MEMORY_DEFAULT_STATE_IS_DISABLED
    config.SIM_MEMORY_DEFAULT_STATE_IS_DISABLED = (
        False  # DANGEROUS: Forcing a misconfiguration for test
    )
    misconfigured_disabler = VaultMemoryDisabler()  # Re-init with bad config
    status_misconfigured = misconfigured_disabler.is_memory_enabled_simulated(
        "vault_beta_002", "critical_action_test"
    )
    print(json.dumps(status_misconfigured, indent=2))
    config.SIM_MEMORY_DEFAULT_STATE_IS_DISABLED = (
        original_default_state  # Reset to safe default
    )
    # Re-initialize with correct config for any further tests if needed
    # disabler = VaultMemoryDisabler()

    logger.info("--- VaultMemoryDisabler Example Finished ---")
