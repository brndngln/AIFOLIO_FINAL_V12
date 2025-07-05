# V80 Automation Queue Engine — Static, SAFE AI, Owner-Controlled
# Batches, schedules, groups, and logs all automations for next 24h
# No sentience, no recursion, no adaptation

import datetime


class AutomationQueue:
    _queue = []
    _history = []

    @staticmethod
    def add(task):
        AutomationQueue._queue.append(
            {"task": task, "added": datetime.datetime.utcnow().isoformat()}
        )
        AutomationQueue._history.append(
            {
                "event": "add",
                "task": task,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def get_queue():
        return list(AutomationQueue._queue)

    @staticmethod
    def get_next_24h():
        # Return all tasks scheduled for next 24h
        now = datetime.datetime.utcnow()
        return [
            item
            for item in AutomationQueue._queue
            if "schedule" not in item
            or (now <= item["schedule"] <= now + datetime.timedelta(hours=24))
        ]

    @staticmethod
    def cancel(task_id):
        AutomationQueue._queue = [
            item for item in AutomationQueue._queue if item.get("id") != task_id
        ]
        AutomationQueue._history.append(
            {
                "event": "cancel",
                "task_id": task_id,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )

    @staticmethod
    def pause(task_id):
        for item in AutomationQueue._queue:
            if item.get("id") == task_id:
                item["paused"] = True
                AutomationQueue._history.append(
                    {
                        "event": "pause",
                        "task_id": task_id,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                    }
                )

    @staticmethod
    def retry(task_id):
        for item in AutomationQueue._queue:
            if item.get("id") == task_id:
                item["paused"] = False
                AutomationQueue._history.append(
                    {
                        "event": "retry",
                        "task_id": task_id,
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                    }
                )

    @staticmethod
    def log():
        return list(AutomationQueue._history)
