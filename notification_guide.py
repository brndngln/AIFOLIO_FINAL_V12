"""
AIFOLIO™ NOTIFICATION & GUIDE SYSTEM (OWNER AUTHORITY)
Static notification and expert guide controls. All OWNER-controlled and SAFE AI compliant.
"""
import logging
from typing import List

class NotificationSystem:
    def __init__(self):
        self.notifications = []
        self.settings = {
            'type': 'Urgent',  # Urgent | Legal | Business | AI Behavior | Personal | Reminder
            'frequency': 'Immediate',  # Immediate | Hourly Digest | Daily Digest
            'format': 'Visual UI',  # Voice | Visual UI | Email | Telegram | PDF Summary
            'authority': 'Needs Approval'  # Needs Approval | Passive Log Only | Auto-Execute
        }

    def send_notification(self, message: str, ntype=None):
        ntype = ntype or self.settings['type']
        logging.info(f'[NOTIFY] {ntype}: {message}')
        self.notifications.append((ntype, message))
        return True

    def set_settings(self, type=None, frequency=None, format=None, authority=None):
        if type: self.settings['type'] = type
        if frequency: self.settings['frequency'] = frequency
        if format: self.settings['format'] = format
        if authority: self.settings['authority'] = authority
        return self.settings

class ExpertGuide:
    def __init__(self):
        self.guides = {}
        self.enabled = True

    def add_guide(self, screen: str, guide_text: str):
        self.guides[screen] = guide_text

    def get_guide(self, screen: str):
        if self.enabled and screen in self.guides:
            return self.guides[screen]
        return None

    def toggle(self, enabled: bool):
        self.enabled = enabled
        return self.enabled
