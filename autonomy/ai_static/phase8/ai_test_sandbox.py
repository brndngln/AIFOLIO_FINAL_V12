"""
SAFE AI Static Module: AI Test Sandbox
- Isolated, static test environment for new AI modules
- No production impact, logs all test runs
- No recursion, no adaptive logic
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/ai_test_sandbox_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


def run_ai_sandbox_test(module_name, test_case, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    event = f"[{timestamp}] SANDBOX TEST: {module_name} | Test: {test_case} | Triggered by: {triggered_by}"
    logging.info(event)
    return event
