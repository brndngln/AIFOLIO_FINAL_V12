"""
AIFOLIO™ SAFE AI MODULE: Load Balancer Stub
- Static, non-sentient
- Logs task queue distribution events
- No dynamic routing or static scaling
"""
import logging

LOG_PATH = "../../distribution/legal_exports/load_balancer_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def log_task_distribution(task_id, queue):
    logging.info(f"Task {task_id} assigned to queue {queue}")
