import queue
import threading
import random
import time
import os
import json
import datetime
from typing import Callable, Any

BALANCER_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/load_balancer_log.jsonl")
)
os.makedirs(os.path.dirname(BALANCER_LOG), exist_ok=True)


# --- Load Balancer for AI Task Queue ---
from typing import Callable, Any, List

class AITaskQueue:
    queue: "queue.Queue[Callable[..., Any]]"
    workers: int
    threads: List[threading.Thread]
    def __init__(self, workers: int = 3) -> None:
        self.queue: queue.Queue[Callable[..., Any]] = queue.Queue()
        self.workers: int = workers
        self.threads: List[threading.Thread] = []

    def add_task(self, task: Callable[..., Any]) -> None:
        self.queue.put(task)

    def worker(self) -> None:
        while True:
            task = self.queue.get()
            try:
                # Simulate task execution
                result = task()
                status = "success"
            except Exception as e:
                result = str(e)
                status = "fail"
            entry = {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "task": str(task),
                "result": result,
                "status": status,
            }
            with open(BALANCER_LOG, "a") as f:
                f.write(json.dumps(entry) + "\n")
            self.queue.task_done()

    def start(self) -> None:
        for _ in range(self.workers):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            self.threads.append(t)


if __name__ == "__main__":
    balancer = AITaskQueue(workers=2)
    balancer.start()
    balancer.add_task(lambda: time.sleep(random.uniform(0.1, 0.5)))
    balancer.add_task(lambda: 1 / 0)  # Simulate failure
    time.sleep(1)
