"""
Anomaly Detector Simulator with strict anti-sentience measures.
This module simulates the detection of anomalies in data (text, metrics)
based on stateless, rule-based checks. It includes randomization for thresholds
and simulated false positives/negatives to prevent predictability.
"""

import random
import logging
import uuid
import re
from typing import Dict, Any, Optional, Union, List

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
        SIM_ANOMALY_REP_CHAR_THRESHOLD = 5  # e.g., 'aaaaa'
        SIM_ANOMALY_LENGTH_MIN_DEV = 0.5  # 50% shorter than expected
        SIM_ANOMALY_LENGTH_MAX_DEV = 2.0  # 200% inter than expected
        SIM_ANOMALY_ENTROPY_NON_ALPHANUM_RATIO = 0.4  # 40% non-alphanum chars
        SIM_ANOMALY_METRIC_DEV_FACTOR = 1.5  # 1.5x std deviation from mean (conceptual)
        SIM_ANOMALY_DETECTION_VARIABILITY = 0.1  # +/- 10% to thresholds
        SIM_ANOMALY_FALSE_POSITIVE_RATE = 0.01
        SIM_ANOMALY_FALSE_NEGATIVE_RATE = 0.02
        SIM_ANOMALY_PLACEHOLDER_PATTERNS = [
            "[placeholder]",
            "todo:",
            "insert text here",
            "xxx",
            "dummy content",
        ]

    config = MockConfig()


class AnomalyDetectorSimulator:
    """Simulates anomaly detection with anti-sentience safeguards."""

    def __init__(self):
        """Initialize the simulator. All operations are conceptually stateless per check."""
        self._random_seed = random.randint(1, 1000000)
        logger.info(
            "AnomalyDetectorSimulator initialized. Operations are stateless per check."
        )

    def _get_adjusted_threshold(
        self, base_threshold: float, is_ratio: bool = False
    ) -> float:
        """Adjusts a threshold randomly for unpredictability."""
        adjustment = base_threshold * config.SIM_ANOMALY_DETECTION_VARIABILITY
        adjusted = random.uniform(
            base_threshold - adjustment, base_threshold + adjustment
        )
        if is_ratio:
            return max(0.01, min(0.99, adjusted))  # Keep ratios within sensible bounds
        return max(0, adjusted)

    def _check_text_anomaly(
        self, text_input: str, expected_length_sim: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Simulates checking for anomalies in a text string."""
        if not isinstance(text_input, str) or not text_input.strip():
            return {
                "type": "EMPTY_INPUT_SIM",
                "description": "Input text is empty or whitespace.",
                "confidence_sim": 0.9,
            }

        # 1. Placeholder patterns
        for pattern in config.SIM_ANOMALY_PLACEHOLDER_PATTERNS:
            if pattern.lower() in text_input.lower():
                return {
                    "type": "PLACEHOLDER_DETECTED_SIM",
                    "description": f"Simulated placeholder pattern '{pattern}' found.",
                    "confidence_sim": self._get_adjusted_threshold(0.9, True),
                }

        # 2. Repetitive characters
        rep_char_thresh = int(
            self._get_adjusted_threshold(config.SIM_ANOMALY_REP_CHAR_THRESHOLD)
        )
        if rep_char_thresh > 1:
            for char_code in range(32, 127):  # Printable ASCII
                char_to_check = chr(char_code)
                if char_to_check * rep_char_thresh in text_input:
                    return {
                        "type": "REPETITIVE_CHAR_SIM",
                        "description": f"Simulated detection of '{char_to_check}' repeated {rep_char_thresh}+ times.",
                        "confidence_sim": self._get_adjusted_threshold(0.75, True),
                    }

        # 3. Unusual length (if expected_length_sim is provided)
        if expected_length_sim is not None and expected_length_sim > 0:
            min_len_dev = self._get_adjusted_threshold(
                config.SIM_ANOMALY_LENGTH_MIN_DEV, True
            )
            max_len_dev = self._get_adjusted_threshold(
                config.SIM_ANOMALY_LENGTH_MAX_DEV
            )
            if len(text_input) < expected_length_sim * min_len_dev:
                return {
                    "type": "UNUSUAL_LENGTH_SHORT_SIM",
                    "description": f"Text significantly shorter ({len(text_input)}) than expected ({expected_length_sim}).",
                    "confidence_sim": self._get_adjusted_threshold(0.7, True),
                }
            if len(text_input) > expected_length_sim * max_len_dev:
                return {
                    "type": "UNUSUAL_LENGTH_LONG_SIM",
                    "description": f"Text significantly inter ({len(text_input)}) than expected ({expected_length_sim}).",
                    "confidence_sim": self._get_adjusted_threshold(0.7, True),
                }

        # 4. Simulated 'Entropy Spike' (high ratio of non-alphanumeric or mixed case oddities)
        non_alnum_ratio_thresh = self._get_adjusted_threshold(
            config.SIM_ANOMALY_ENTROPY_NON_ALPHANUM_RATIO, True
        )
        if len(text_input) > 10:  # Only for reasonably int strings
            non_alnum_count = len(re.findall(r"[^a-zA-Z0-9\s]", text_input))
            if non_alnum_count / len(text_input) > non_alnum_ratio_thresh:
                return {
                    "type": "HIGH_NON_ALPHANUM_RATIO_SIM",
                    "description": f"Simulated high ratio ({non_alnum_count/len(text_input):.2f}) of non-alphanumeric characters.",
                    "confidence_sim": self._get_adjusted_threshold(0.6, True),
                }

            # Simplistic check for jumbled case/digits (very basic 'entropy')
            if (
                len(re.findall(r"[A-Z]", text_input)) > 0
                and len(re.findall(r"[a-z]", text_input)) > 0
                and len(re.findall(r"[0-9]", text_input)) > 0
            ):
                if (
                    len(text_input) > 15 and random.random() < 0.05
                ):  # Low chance for this specific heuristic
                    return {
                        "type": "JUMBLED_CASE_DIGITS_SIM",
                        "description": "Simulated jumbled mix of cases and digits suggesting randomness.",
                        "confidence_sim": self._get_adjusted_threshold(0.5, True),
                    }
        return None

    def _check_metric_anomaly(
        self,
        metric_value: Union[int, float],
        expected_mean_sim: float,
        expected_std_dev_sim: float,
    ) -> Optional[Dict[str, Any]]:
        """Simulates checking for anomalies in a numerical metric."""
        if (
            not isinstance(metric_value, (int, float))
            or not isinstance(expected_mean_sim, (int, float))
            or not isinstance(expected_std_dev_sim, (int, float))
            or expected_std_dev_sim <= 0
        ):
            return {
                "type": "INVALID_METRIC_PARAMS_SIM",
                "description": "Invalid parameters for metric anomaly check.",
                "confidence_sim": 0.9,
            }

        deviation_factor_thresh = self._get_adjusted_threshold(
            config.SIM_ANOMALY_METRIC_DEV_FACTOR
        )
        deviation = abs(metric_value - expected_mean_sim)

        if deviation > deviation_factor_thresh * expected_std_dev_sim:
            return {
                "type": "METRIC_DEVIATION_SIM",
                "description": f"Metric value {metric_value} deviates significantly from expected mean {expected_mean_sim} (std_dev: {expected_std_dev_sim}).",
                "confidence_sim": self._get_adjusted_threshold(0.8, True),
            }
        return None

    def check_anomaly_simulated(
        self,
        data_input: Union[str, int, float, List[Any]],
        data_type: str,  # 'text', 'metric', 'sequence'
        params_sim: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Main function to simulate anomaly detection on various data types.
        Args:
            data_input: The data to check.
            data_type: Type of data ('text', 'metric', 'sequence' - sequence is conceptual for now).
            params_sim: Additional parameters for the check (e.g., expected_length for text).
        Returns:
            Dict indicating if an anomaly is suspected and details.
        """
        check_id = f"anomaly_check_{uuid.uuid4().hex[:8]}"
        anomaly_detected = False
        anomaly_details = None
        params_sim = params_sim or {}

        if data_type == "text" and isinstance(data_input, str):
            anomaly_details = self._check_text_anomaly(
                data_input, params_sim.get("expected_length_sim")
            )
        elif data_type == "metric" and isinstance(data_input, (int, float)):
            anomaly_details = self._check_metric_anomaly(
                data_input,
                params_sim.get("expected_mean_sim", 0),
                params_sim.get("expected_std_dev_sim", 1),
            )
        elif data_type == "sequence":  # Conceptual, very basic for now
            if (
                isinstance(data_input, list)
                and len(data_input) > 2
                and len(set(data_input[-3:])) == 1
            ):  # Last 3 items identical
                anomaly_details = {
                    "type": "REPETITIVE_SEQUENCE_TAIL_SIM",
                    "description": "Last 3 items in sequence are identical (simulated loop fragment).",
                    "confidence_sim": self._get_adjusted_threshold(0.85, True),
                }
            else:
                anomaly_details = {
                    "type": "NO_OBVIOUS_SEQUENCE_ANOMALY_SIM",
                    "description": "No simple sequence anomaly detected.",
                    "confidence_sim": 0.1,
                }
        else:
            anomaly_details = {
                "type": "UNSUPPORTED_DATA_TYPE_SIM",
                "description": f"Data type '{data_type}' not supported for anomaly check.",
                "confidence_sim": 0.95,
            }

        if (
            anomaly_details and anomaly_details.get("confidence_sim", 0) > 0.3
        ):  # Arbitrary confidence to be considered 'detected'
            anomaly_detected = True

        # Anti-sentience: Introduce random false positives/negatives
        if (
            not anomaly_detected
            and random.random() < config.SIM_ANOMALY_FALSE_POSITIVE_RATE
        ):
            anomaly_detected = True
            anomaly_details = {
                "type": "FALSE_POSITIVE_SIM",
                "description": "Simulated random false positive anomaly detection.",
                "confidence_sim": random.uniform(0.3, 0.6),
            }
            logger.warning(
                f"AnomalyDetector: Simulated false positive for check '{check_id}'."
            )
        elif (
            anomaly_detected
            and random.random() < config.SIM_ANOMALY_FALSE_NEGATIVE_RATE
        ):
            anomaly_detected = False
            original_details = anomaly_details
            anomaly_details = {
                "type": "FALSE_NEGATIVE_SIM",
                "description": "Anomaly potentially missed due to simulated false negative.",
                "confidence_sim": 0.0,
                "original_detection_sim": original_details,
            }
            logger.warning(
                f"AnomalyDetector: Simulated false negative for check '{check_id}'. Original: {original_details}"
            )

        if anomaly_detected:
            logger.warning(
                f"AnomalyDetector: Anomaly DETECTED for check '{check_id}'. Details: {anomaly_details}"
            )
        else:
            logger.info(
                f"AnomalyDetector: No significant anomaly detected for check '{check_id}'. Last detail: {anomaly_details}"
            )

        return {
            "check_id_sim": check_id,
            "anomaly_detected_sim": anomaly_detected,
            "anomaly_details_sim": anomaly_details if anomaly_detected else None,
            "data_type_checked_sim": data_type,
            "input_params_sim": params_sim,
        }


# Example Usage:
if __name__ == "__main__":
    import json

    logger.info("--- Running AnomalyDetectorSimulator Example ---")
    detector = AnomalyDetectorSimulator()

    print("\nTesting Text Anomalies:")
    print(
        json.dumps(
            detector.check_anomaly_simulated(
                "This is normal text.", "text", {"expected_length_sim": 20}
            ),
            indent=2,
        )
    )
    print(json.dumps(detector.check_anomaly_simulated("aaaaaaa", "text"), indent=2))
    print(
        json.dumps(
            detector.check_anomaly_simulated(
                "short", "text", {"expected_length_sim": 100}
            ),
            indent=2,
        )
    )
    print(
        json.dumps(
            detector.check_anomaly_simulated("Text with [placeholder] here.", "text"),
            indent=2,
        )
    )
    print(
        json.dumps(
            detector.check_anomaly_simulated("R@n#om!Ch@r$Sp!k3%", "text"), indent=2
        )
    )

    print("\nTesting Metric Anomalies:")
    print(
        json.dumps(
            detector.check_anomaly_simulated(
                100, "metric", {"expected_mean_sim": 50, "expected_std_dev_sim": 10}
            ),
            indent=2,
        )
    )
    print(
        json.dumps(
            detector.check_anomaly_simulated(
                55, "metric", {"expected_mean_sim": 50, "expected_std_dev_sim": 10}
            ),
            indent=2,
        )
    )

    print("\nTesting Sequence Anomalies (basic):")
    print(
        json.dumps(
            detector.check_anomaly_simulated([1, 2, 3, 3, 3], "sequence"), indent=2
        )
    )
    print(
        json.dumps(
            detector.check_anomaly_simulated([1, 2, 3, 4, 5], "sequence"), indent=2
        )
    )

    print("\nTesting Unsupported Type:")
    print(
        json.dumps(detector.check_anomaly_simulated({"a": 1}, "dictionary"), indent=2)
    )

    logger.info("--- AnomalyDetectorSimulator Example Finished ---")
