import json
import os
import logging
from datetime import datetime
from importlib import import_module
from core.logic.fallback_handler import FallbackHandler
from core.logic.compliance_engine import ComplianceEngine
from core.logic.vault_manager import VaultManager
from integrations.webhooks import send_webhook, split_signal
from integrations.slack_alerts import send_slack_alert
from automation.n8n_bridge import send_n8n_event
import redis
import sqlite3

REDIS_URL = os.getenv('REDIS_URL')
DB_PATH = os.getenv('AUTOMATION_DB', 'automation.db')
EVENT_MAP_PATH = os.path.join(os.path.dirname(__file__), '../config/event_map.json')

class EventRouter:
    def __init__(self):
        self.fallback = FallbackHandler()
        self.compliance = ComplianceEngine()
        self.vault = VaultManager()
        self.redis = redis.Redis.from_url(REDIS_URL) if REDIS_URL else None
        self.db = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.event_map = self.load_event_map()

    def load_event_map(self):
        if os.path.exists(EVENT_MAP_PATH):
            with open(EVENT_MAP_PATH, 'r') as f:
                return json.load(f)
        return {}

    def route(self, event_type, payload, options=None):
        ts = datetime.utcnow().isoformat()
        log_entry = {'event': event_type, 'payload': payload, 'timestamp': ts}
        try:
            self.log_event(log_entry)
            logic = self.event_map.get(event_type, [])
            for action in logic:
                if isinstance(action, dict) and 'if' in action:
                    # Conditional gateway
                    if not self.evaluate_condition(action['if'], payload):
                        continue
                    action = action['then']
                self.execute_action(action, payload)
            # Signal splitter
            if options and options.get('split'):
                split_signal(event_type, payload, options['split'])
        except Exception as e:
            logging.error(f"EventRouter error: {e}")
            self.fallback.handle(event_type, payload, error=str(e))

    def execute_action(self, action, payload):
        if action == 'webhook':
            send_webhook(payload)
        elif action == 'slack':
            send_slack_alert(payload)
        elif action == 'n8n':
            send_n8n_event(payload)
        elif action == 'compliance':
            self.compliance.process(payload)
        elif action == 'vault':
            self.vault.process(payload)
        elif action == 'log':
            self.log_event({'event': 'custom_log', 'payload': payload, 'timestamp': datetime.utcnow().isoformat()})
        # Add more integrations as needed

    def evaluate_condition(self, condition, payload):
        # Example: {'field': 'revenue', 'op': '>', 'value': 100}
        try:
            field, op, value = condition['field'], condition['op'], condition['value']
            actual = payload.get(field)
            if op == '>': return actual > value
            if op == '>=': return actual >= value
            if op == '<': return actual < value
            if op == '<=': return actual <= value
            if op == '==': return actual == value
            if op == '!=': return actual != value
        except Exception as e:
            logging.warning(f"Condition eval failed: {e}")
        return False

    def log_event(self, entry):
        # Redis for async replay, SQLite for persistence
        try:
            if self.redis:
                self.redis.rpush('event_log', json.dumps(entry))
            cursor = self.db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS event_log (ts TEXT, event TEXT, payload TEXT)')
            cursor.execute('INSERT INTO event_log (ts, event, payload) VALUES (?, ?, ?)',
                           (entry['timestamp'], entry['event'], json.dumps(entry['payload'])))
            self.db.commit()
        except Exception as e:
            logging.warning(f"Log event failed: {e}")

    def manual_retrigger(self, event_type, payload):
        self.route(event_type, payload)
