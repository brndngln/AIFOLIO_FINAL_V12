#!/usr/bin/env python3
"""
AIFOLIO Sentinel Monitoring System
=================================

Real-time monitoring and alerting for AI system behavior.
"""

import json
import logging
import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass
class SecurityEvent:
    """Security event data structure."""

    event_type: str
    severity: str
    source: str
    details: Dict[str, Any]
    timestamp: float


class SentinelMonitor:
    """Advanced monitoring system for AI containment."""

    def __init__(self):
        self.logger = logging.getLogger("sentinel_monitor")
        self.events = []
        self.alert_thresholds = {
            "high_complexity": 15,
            "security_violations": 5,
            "ethical_violations": 1,
        }

    def log_security_event(
        self, event_type: str, severity: str, source: str, details: Dict[str, Any]
    ) -> None:
        """Log a security event."""
        event = SecurityEvent(
            event_type=event_type,
            severity=severity,
            source=source,
            details=details,
            timestamp=time.time(),
        )

        self.events.append(event)
        self.logger.info(f"Security event: {event}")

        # Check if alert threshold is exceeded
        if self._should_alert(event):
            self._trigger_alert(event)

    def _should_alert(self, event: SecurityEvent) -> bool:
        """Determine if an event should trigger an alert."""
        if event.severity == "CRITICAL":
            return True

        # Count recent events of same type
        recent_events = [
            e for e in self.events[-100:] if e.event_type == event.event_type
        ]
        return len(recent_events) > self.alert_thresholds.get(event.event_type, 10)

    def _trigger_alert(self, event: SecurityEvent) -> None:
        """Trigger security alert."""
        self.logger.critical(f"SECURITY ALERT: {event}")

        # Save alert to file
        alert_file = pathlib.Path("monitoring") / "security_alerts.json"
        alerts = []

        if alert_file.exists():
            with open(alert_file, "r") as f:
                alerts = json.load(f)

        alerts.append(asdict(event))

        with open(alert_file, "w") as f:
            json.dump(alerts, f, indent=2)

    def get_security_summary(self) -> Dict[str, Any]:
        """Get security monitoring summary."""
        return {
            "total_events": len(self.events),
            "critical_events": len(
                [e for e in self.events if e.severity == "CRITICAL"]
            ),
            "recent_events": len(
                [e for e in self.events if time.time() - e.timestamp < 3600]
            ),
            "event_types": list(set(e.event_type for e in self.events)),
        }


# Global sentinel monitor
sentinel = SentinelMonitor()
