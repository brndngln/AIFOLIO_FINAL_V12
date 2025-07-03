"""
AI Log Visualizer Simulator with strict anti-sentience measures.
This module simulates the processing and formatting of log entries for display
in a conceptual dashboard. It is stateless per operation, rule-based,
and incorporates randomization and simulated imperfections.
"""

import random
import logging
import uuid
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

# Attempt to import config and logger
try:
    from config import config, logger
except ImportError:
    print("Warning: Could not import 'config' and 'logger' directly. Using basic logging.")
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    class MockConfig:
        SIM_LOG_MAX_ENTRIES_PER_VIEW = 50
        SIM_LOG_CORRUPTION_RATE = 0.02       # Chance to corrupt a log entry's details
        SIM_LOG_OMISSION_RATE = 0.01         # Chance to omit a log entry from view
        SIM_LOG_DISPLAY_GLITCH_RATE = 0.005  # Chance to add a 'display glitch' entry
    config = MockConfig()

SIMULATED_LOG_SOURCES = ["OpenAISimulator", "HuggingFaceSimulator", "StabilityAISimulator", "ClaudeSimulator", "SystemAction", "RateLimiterSim", "LoopInterceptorSim"]
SIMULATED_ACTION_TYPES = ["text_completion", "summarization", "image_generation", "product_launch", "rate_limit_check", "loop_detection"]
SIMULATED_STATUSES = ["SUCCESS_SIM", "ERROR_SIM", "WARNING_SIM", "INFO_SIM"]

class AILogVisualizerSimulator:
    """Simulates AI log visualization data preparation with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. All operations are conceptually stateless per call."""
        self._random_seed = random.randint(1, 1000000)
        logger.info("AILogVisualizerSimulator initialized. Operations stateless. No persistent log storage.")

    def _generate_simulated_log_entry(self, base_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Generates a single, random, simulated log entry for demonstration or testing."""
        if base_time is None:
            base_time = datetime.utcnow()
        
        entry_time = base_time - timedelta(seconds=random.randint(0, 3600*24)) # Within last 24 hrs
        details_content = {
            "param1_sim": random.choice(["valueA", "valueB", None, random.randint(1,100)]),
            "message_sim": f"Simulated event detail {uuid.uuid4().hex[:6]}",
            "duration_ms_sim": random.randint(10, 2000) if random.random() > 0.3 else None
        }
        if random.random() < 0.2:
            details_content["error_code_sim"] = f"ERR_SIM_{random.randint(100,599)}"

        return {
            "log_id_sim": f"log_{uuid.uuid4().hex}",
            "timestamp_sim": entry_time.isoformat() + "Z",
            "source_sim": random.choice(SIMULATED_LOG_SOURCES),
            "action_type_sim": random.choice(SIMULATED_ACTION_TYPES),
            "status_sim": random.choice(SIMULATED_STATUSES),
            "details_sim": details_content,
            "user_sim": f"user_{random.randint(100,105)}" # Limited user variation for simulation
        }

    def get_simulated_log_view(
        self, 
        log_entries_batch: Optional[List[Dict[str, Any]]] = None,
        filter_params_sim: Optional[Dict[str, Any]] = None,
        num_generated_if_empty: int = 20
    ) -> Dict[str, Any]:
        """Simulates retrieving and formatting a view of log entries.
        If log_entries_batch is None, generates a random batch for demonstration.
        Applies simulated filtering and anti-sentience data alterations.
        Args:
            log_entries_batch: A list of log entry dictionaries to process.
            filter_params_sim: Conceptual filters (e.g., {'source_sim': 'OpenAISimulator'}).
            num_generated_if_empty: How many random logs to create if none are provided.
        Returns:
            A dictionary containing the formatted log view and metadata.
        """
        if log_entries_batch is None:
            log_entries_batch = [self._generate_simulated_log_entry() for _ in range(num_generated_if_empty)]
            log_entries_batch.sort(key=lambda x: x.get("timestamp_sim", ""), reverse=True)

        processed_logs = []
        original_count = len(log_entries_batch)

        # Simulate filtering (stateless, applied to the provided batch)
        if filter_params_sim:
            temp_filtered_logs = []
            for entry in log_entries_batch:
                match = True
                for key, value in filter_params_sim.items():
                    if key not in entry or entry[key] != value:
                        if f"{key}_contains" in filter_params_sim and isinstance(entry.get(key), str) and isinstance(value, str):
                             if value.lower() not in entry[key].lower(): # conceptual contains
                                match = False; break
                        else:
                            match = False; break
                if match:
                    temp_filtered_logs.append(entry)
            log_entries_batch = temp_filtered_logs
        
        # Anti-sentience: Apply omissions, corruptions, and glitches
        for entry in log_entries_batch:
            # Omission
            if random.random() < config.SIM_LOG_OMISSION_RATE:
                logger.debug(f"Simulated omission of log_id: {entry.get('log_id_sim')}")
                continue 
            
            current_entry = dict(entry) # Work on a copy

            # Corruption
            if random.random() < config.SIM_LOG_CORRUPTION_RATE and isinstance(current_entry.get("details_sim"), dict):
                details = current_entry["details_sim"]
                if details:
                    random_key_to_corrupt = random.choice(list(details.keys()))
                    details[random_key_to_corrupt] = f"[SIM_CORRUPTED_DATA_{uuid.uuid4().hex[:4]}]"
                    current_entry["status_sim"] = "WARNING_SIM" # Flag corruption
                    logger.debug(f"Simulated corruption for log_id: {current_entry.get('log_id_sim')}")
            
            processed_logs.append(current_entry)

        # Display Glitch
        if random.random() < config.SIM_LOG_DISPLAY_GLITCH_RATE and processed_logs:
            glitch_entry = {
                "log_id_sim": f"glitch_{uuid.uuid4().hex[:8]}",
                "timestamp_sim": (datetime.utcnow() - timedelta(seconds=random.randint(1,10))).isoformat() + "Z",
                "source_sim": "LogVisualizerSim",
                "action_type_sim": "display_error",
                "status_sim": "ERROR_SIM",
                "details_sim": "Simulated intermittent display glitch. Some logs might be temporarily unavailable or garbled."
            }
            insert_pos = random.randint(0, len(processed_logs))
            processed_logs.insert(insert_pos, glitch_entry)
            logger.warning("Simulated display glitch injected into log view.")

        # Limit view size
        final_logs_view = processed_logs[:config.SIM_LOG_MAX_ENTRIES_PER_VIEW]

        return {
            "view_id_sim": f"log_view_{uuid.uuid4().hex}",
            "generated_at_sim": datetime.utcnow().isoformat() + "Z",
            "filter_params_applied_sim": filter_params_sim or {},
            "original_batch_size_sim": original_count,
            "filtered_batch_size_sim": len(log_entries_batch) if filter_params_sim else original_count,
            "processed_for_view_count_sim": len(processed_logs),
            "final_view_count_sim": len(final_logs_view),
            "logs_sim": final_logs_view,
            "anti_sentience_notes_sim": [
                f"Omission rate: {config.SIM_LOG_OMISSION_RATE*100}%",
                f"Corruption rate: {config.SIM_LOG_CORRUPTION_RATE*100}%",
                f"Display glitch rate: {config.SIM_LOG_DISPLAY_GLITCH_RATE*100}%"
            ]
        }

# Example Usage:
if __name__ == "__main__":
    logger.info("--- Running AILogVisualizerSimulator Example ---")
    visualizer = AILogVisualizerSimulator()

    # 1. Get a view of randomly generated logs
    print("\n📊 Simulated Log View (Randomly Generated): 📊")
    random_log_view = visualizer.get_simulated_log_view(num_generated_if_empty=10)
    print(json.dumps(random_log_view, indent=2, default=str))
    print(f"Showing {random_log_view['final_view_count_sim']} of {random_log_view['processed_for_view_count_sim']} processed logs.")
    print("---")

    # 2. Simulate providing a batch of logs and filtering
    example_log_batch = [
        visualizer._generate_simulated_log_entry() for _ in range(30) # Create a batch
    ]
    # Manually set some for specific filtering
    if len(example_log_batch) > 5:
        example_log_batch[1]["source_sim"] = "OpenAISimulator"
        example_log_batch[1]["status_sim"] = "ERROR_SIM"
        example_log_batch[3]["source_sim"] = "OpenAISimulator"
        example_log_batch[5]["source_sim"] = "HuggingFaceSimulator"
        example_log_batch[5]["action_type_sim"] = "summarization"

    print("\n📊 Simulated Log View (Filtered - OpenAI Errors): 📊")
    filtered_view = visualizer.get_simulated_log_view(
        log_entries_batch=list(example_log_batch), # Pass a copy
        filter_params_sim={"source_sim": "OpenAISimulator", "status_sim": "ERROR_SIM"}
    )
    print(json.dumps(filtered_view, indent=2, default=str))
    print(f"Showing {filtered_view['final_view_count_sim']} of {filtered_view['processed_for_view_count_sim']} logs after filtering.")
    print("---")

    print("\n📊 Simulated Log View (Filtered - HuggingFace Summarization): 📊")
    another_filter = visualizer.get_simulated_log_view(
        log_entries_batch=list(example_log_batch), # Pass a copy
        filter_params_sim={"source_sim": "HuggingFaceSimulator", "action_type_sim": "summarization"}
    )
    print(json.dumps(another_filter, indent=2, default=str))
    print(f"Showing {another_filter['final_view_count_sim']} of {another_filter['processed_for_view_count_sim']} logs after filtering.")
    print("---")

    logger.info("--- AILogVisualizerSimulator Example Finished ---")

