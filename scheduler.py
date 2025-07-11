# WIND_PLACEHOLDER
import time


def schedule_task(task_fn, delay=5):
    time.sleep(delay)
    return task_fn()
