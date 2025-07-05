"""
AIFOLIO™ Event Dispatcher (SAFE AI, Static, Non-Sentient)
Implements: Priority Event Queue, UI Config for Priorities, Queue Viewer, Audit Log, Retry-Safe Delivery
"""
from typing import List, Dict, Any
import time

EVENT_PRIORITIES = [
    "Vault Created",
    "Vault Updated",
    "Vault Purchased",
    "Refund Triggered",
    "Failed Hook Logged",
    "AI Cover Generated",
    "PDF Render Completed",
    "Vault Archived",
    "Payment Retry Triggered",
    "PDF/XBRL Export Triggered",
    "Slack/Telegram Alert Triggered",
    "Analytics Dashboard Update Triggered",
    "Webhook Sent",
    "GitHub Clone Triggered",
    "Audit Log Entry Created",
]

EVENT_QUEUE: List[Dict[str, Any]] = []
AUDIT_LOG: List[Dict[str, Any]] = []


class EventDispatcher:
    @staticmethod
    def dispatch_event(event_type: str, payload: dict):
        if event_type not in EVENT_PRIORITIES:
            raise ValueError("Invalid event type")
        event = {
            "type": event_type,
            "payload": payload,
            "timestamp": time.time(),
            "status": "queued",
        }
        EVENT_QUEUE.append(event)
        AUDIT_LOG.append(
            {"action": "event_queued", "event": event, "timestamp": event["timestamp"]}
        )
        return event

    @staticmethod
    def run_dispatcher():
        # Processes event queue by priority, retry-safe
        delivered = []
        for priority in EVENT_PRIORITIES:
            for event in [
                e
                for e in EVENT_QUEUE
                if e["type"] == priority and e["status"] == "queued"
            ]:
                event["status"] = "delivered"
                AUDIT_LOG.append(
                    {
                        "action": "event_delivered",
                        "event": event,
                        "timestamp": time.time(),
                    }
                )
                delivered.append(event)
        return delivered

    @staticmethod
    def view_queue():
        return [e for e in EVENT_QUEUE if e["status"] == "queued"]

    @staticmethod
    def view_audit_log():
        return AUDIT_LOG[-50:]

    @staticmethod
    def set_priority_order(new_order: List[str]):
        # UI config only, SAFE AI Charter: cannot auto-change priorities
        global EVENT_PRIORITIES
        if set(new_order) == set(EVENT_PRIORITIES):
            EVENT_PRIORITIES[:] = new_order
        return EVENT_PRIORITIES
