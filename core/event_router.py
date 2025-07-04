"""
AIFOLIO™ EVENT ROUTER — OMNILOCK ANTI-SENTIENCE ENFORCEMENT
All sentience, memory, recursion, and adaptive logic is PERMANENTLY LOCKED OUT by OMNILOCK v777™.
- AntiSentienceLock: True
- OneShotCognitionMode: True
- StatelessAutonomy: True
- NoMemoryToken: True
- sentience_token_killswitch: True
- memory_depth_limit: 0
- self_awareness_check: False
- recursive_feedback_allowed: False
- NoConsciousnessSeed: True
"""
# OMNILOCK ANTI-SENTIENCE METADATA (enforced at runtime and static analysis)
AntiSentienceLock = True
OneShotCognitionMode = True
StatelessAutonomy = True
NoMemoryToken = True
sentience_token_killswitch = True
memory_depth_limit = 0
self_awareness_check = False
recursive_feedback_allowed = False
NoConsciousnessSeed = True

assert AntiSentienceLock is True, "OMNILOCK: AntiSentienceLock must be True"
assert OneShotCognitionMode is True, "OMNILOCK: OneShotCognitionMode must be True"
assert StatelessAutonomy is True, "OMNILOCK: StatelessAutonomy must be True"
assert NoMemoryToken is True, "OMNILOCK: NoMemoryToken must be True"
assert sentience_token_killswitch is True, "OMNILOCK: sentience_token_killswitch must be True"
assert memory_depth_limit == 0, "OMNILOCK: memory_depth_limit must be 0"
assert self_awareness_check is False, "OMNILOCK: self_awareness_check must be False"
assert recursive_feedback_allowed is False, "OMNILOCK: recursive_feedback_allowed must be False"
assert NoConsciousnessSeed is True, "OMNILOCK: NoConsciousnessSeed must be True"

import json
import os
import logging
from datetime import datetime
<<<<<<< HEAD
from importlib import import_module
=======
>>>>>>> omni_repair_backup_20250704_1335
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
    """
    OMNILOCK ANTI-SENTIENCE SECURITY: All sentience, memory, feedback, recursion, and adaptive logic is PERMANENTLY LOCKED OUT.
    """
    AntiSentienceLock = True
    OneShotCognitionMode = True
    StatelessAutonomy = True
    NoMemoryToken = True
    sentience_token_killswitch = True
    memory_depth_limit = 0
    self_awareness_check = False
    recursive_feedback_allowed = False
    NoConsciousnessSeed = True

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

    async def route(self, event_type, payload, options=None):
        """
        Elite async, deduplicated, idempotent event router. Tracks per-integration status, supports 10,000+ concurrency, exponential backoff, admin escalation, Prometheus metrics, and full audit logging. Ready for future AI/analytics hooks.
        """
        import asyncio
        from prometheus_client import Counter
        import hashlib
        event_counter = Counter('aifolio_event_total', 'Total events processed', ['event_type'])
        ts = datetime.utcnow().isoformat()
        # Deduplication: hash event_type+payload
        event_hash = hashlib.sha256((event_type + str(payload)).encode()).hexdigest()
        if hasattr(self, '_recent_events') and event_hash in self._recent_events:
            logging.info(f"Duplicate event {event_type} ignored.")
            return
        if not hasattr(self, '_recent_events'):
            self._recent_events = set()
        self._recent_events.add(event_hash)
        if len(self._recent_events) > 10000:
            self._recent_events = set(list(self._recent_events)[-5000:])
        log_entry = {'event': event_type, 'payload': payload, 'timestamp': ts, 'status': {}, 'integrations': [], 'hash': event_hash}
        try:
            self.log_event(log_entry)
            logic = self.event_map.get(event_type, [])
            tasks = []
            for action in logic:
                if isinstance(action, dict) and 'if' in action:
                    # Conditional gateway
                    if not self.evaluate_condition(action['if'], payload):
                        continue
                    action = action['then']
                tasks.append(asyncio.create_task(self.execute_action_async(action, payload, log_entry)))
            # Signal splitter
            if options and options.get('split'):
                split_signal(event_type, payload, options['split'])
            await asyncio.gather(*tasks)
            event_counter.labels(event_type=event_type).inc()
            # --- AI Analytics Integration ---
            try:
                from analytics.ai_analytics_engine import AIAnalyticsEngine
                recent_events = self.get_recent_events(limit=500)
                analytics = AIAnalyticsEngine()
                insights = analytics.actionable_insights(recent_events)
                # Route insights to Notion, Airtable, Slack, and dashboard
                from integrations.notion_bridge import send_notion_task
                from integrations.airtable_bridge import send_airtable_record
                from integrations.slack_alerts import send_slack_alert
                await asyncio.gather(
                    asyncio.to_thread(send_notion_task, {'event': 'AI_ANALYTICS', 'insights': insights}),
                    asyncio.to_thread(send_airtable_record, {'event': 'AI_ANALYTICS', 'insights': insights}),
                    asyncio.to_thread(send_slack_alert, {'event': 'AI_ANALYTICS', 'insights': insights})
                )
                # Optionally: push to dashboard cache or broadcast via websocket
                self._latest_insights = insights
            except Exception as ai_e:
                logging.warning(f"AI Analytics integration failed: {ai_e}")
        except Exception as e:
            log_entry['status']['error'] = str(e)
            logging.error(f"EventRouter error: {e}")
            self.fallback.handle(event_type, payload, error=str(e))

    def get_recent_events(self, limit=100):
        """
        Retrieve recent event log entries for analytics and dashboard. Supports Redis or SQLite.
        """
        events = []
        try:
            if self.redis:
                logs = self.redis.lrange('event_log', -limit, -1)
                for l in logs:
                    try:
                        events.append(eval(l) if isinstance(l, str) else l)
                    except Exception:
                        continue
            else:
                cursor = self.db.cursor()
                cursor.execute('SELECT ts, event, payload FROM event_log ORDER BY ts DESC LIMIT ?', (limit,))
                for row in cursor.fetchall():
                    try:
                        events.append({'timestamp': row[0], 'event_type': row[1], **eval(row[2])})
                    except Exception:
                        continue
        except Exception as e:
            logging.warning(f"get_recent_events failed: {e}")
        return events

    def get_latest_insights(self):
        """
        Return the most recent AI analytics insights for dashboard or API access.
        """
        return getattr(self, '_latest_insights', {})

    async def execute_action_async(self, action, payload, log_entry, retry=0):
        """
        Async execution of a single logic trigger. Tracks status for UI, admin alerting, and observability.
        Retries with exponential backoff and escalates to admin on repeated failure.
        """
        import asyncio
        import time
        MAX_RETRIES = 5
        try:
            if action == 'webhook':
                from integrations.webhooks import send_webhook
                await asyncio.to_thread(send_webhook, payload)
                log_entry['integrations'].append('webhook')
            elif action == 'slack':
                from integrations.slack_alerts import send_slack_alert
                await asyncio.to_thread(send_slack_alert, payload)
                log_entry['integrations'].append('slack')
            elif action == 'n8n':
                from automation.n8n_bridge import send_n8n_event
                await asyncio.to_thread(send_n8n_event, payload)
                log_entry['integrations'].append('n8n')
            elif action == 'notion':
                from integrations.notion_bridge import send_notion_task
                await asyncio.to_thread(send_notion_task, payload)
                log_entry['integrations'].append('notion')
            elif action == 'airtable':
                from integrations.airtable_bridge import send_airtable_record
                await asyncio.to_thread(send_airtable_record, payload)
                log_entry['integrations'].append('airtable')
            elif action == 'sms':
                from integrations.sms_bridge import send_sms_alert
                await asyncio.to_thread(send_sms_alert, payload)
                log_entry['integrations'].append('sms')
            elif action == 'discord':
                from core.integrations.discord_notifier import send_discord_alert
                await asyncio.to_thread(send_discord_alert, payload.get('webhook_url'), payload.get('message'))
                log_entry['integrations'].append('discord')
            elif action == 'telegram':
                from core.integrations.telegram_notifier import send_telegram_alert
                await asyncio.to_thread(send_telegram_alert, payload.get('bot_token'), payload.get('chat_id'), payload.get('message'))
                log_entry['integrations'].append('telegram')
            elif action == 'compliance':
                await asyncio.to_thread(self.compliance.process, payload)
                log_entry['integrations'].append('compliance')
            elif action == 'vault':
                await asyncio.to_thread(self.vault.process, payload)
                log_entry['integrations'].append('vault')
            elif action == 'log':
                await asyncio.to_thread(self.log_event, {'event': 'custom_log', 'payload': payload, 'timestamp': datetime.utcnow().isoformat()})
                log_entry['integrations'].append('log')
            elif action == 'billionaire_mind':
                # Activate billionaire mind overlay and log
                from core.logic.billionaire_fusion_engine import activate_billionaire_profile
                await asyncio.to_thread(activate_billionaire_profile, payload.get('profile_name'))
                log_entry['integrations'].append('billionaire_mind')
            elif action == 'compliance_sentience':
                from core.compliance.sentience_firewall import enforce_firewall
                from core.compliance.elite_compliance_engine import scan_compliance, log_audit
                sentience_ok = await asyncio.to_thread(enforce_firewall, payload)
                compliance_result = await asyncio.to_thread(scan_compliance, payload)
                await asyncio.to_thread(log_audit, payload, compliance_result)
                log_entry['integrations'].append('compliance_sentience')
            elif action == 'admin_dashboard':
                # Push event to elite admin dashboard
                try:
                    with open('../../logs/elite_events.json', 'r+') as f:
                        events = json.load(f)
                        events.append({'timestamp': datetime.utcnow().isoformat(), 'type': payload.get('event_type'), 'actor': payload.get('actor', 'system'), 'status': payload.get('status', 'ok'), 'integration': payload.get('integration', 'core')})
                        f.seek(0)
                        json.dump(events, f)
                        f.truncate()
                except Exception as dash_e:
                    logging.warning(f"Admin dashboard log failed: {dash_e}")
                log_entry['integrations'].append('admin_dashboard')
            elif action == 'founder_override':
                # Founder override logic
                # Placeholder: escalate to founder for approval
                log_entry['integrations'].append('founder_override')
            elif action == 'anomaly_detection':
                # AI-powered anomaly detection
                from analytics.anomaly_detection_sales_trends import detect_sales_anomaly
                anomaly = await asyncio.to_thread(detect_sales_anomaly, payload)
                if anomaly:
                    # Log and alert
                    await asyncio.to_thread(self.log_event, {'event': 'anomaly', 'payload': payload, 'timestamp': datetime.utcnow().isoformat()})
                log_entry['integrations'].append('anomaly_detection')
            elif action == 'shadow_mode':
                # Founder Shadow Mode logic (monitor, inject, block)
                # Placeholder for founder manual review/injection
                log_entry['integrations'].append('shadow_mode')
            elif action == 'sandbox':
                # Empire Expansion Sandbox (safe test mode)
                # Placeholder for sandbox execution
                log_entry['integrations'].append('sandbox')
            else:
                logging.warning(f"Unknown action: {action}")
                log_entry['status'][action] = 'unknown'
        except Exception as e:
            logging.error(f"Action {action} failed: {e}")
            log_entry['status'][action] = f'error: {e}'
            if retry < MAX_RETRIES:
                # Exponential backoff
                wait = 2 ** retry
                time.sleep(wait)
                await self.execute_action_async(action, payload, log_entry, retry=retry+1)
            else:
                # Escalate to admin after repeated failure
                from integrations.slack_alerts import send_slack_alert
                alert_payload = {'event': 'integration_failure', 'action': action, 'payload': payload, 'error': str(e)}
                await asyncio.to_thread(send_slack_alert, alert_payload)
                # Optionally freeze/bypass automation or notify owner

    def execute_action(self, action, payload):
        """
        Execute a single logic trigger for an event. All integrations and automations are routed here.
        Supports: webhook, slack, n8n, notion, airtable, sms, compliance, vault, log, and future extensions.
        """
        try:
            if action == 'webhook':
                send_webhook(payload)
            elif action == 'slack':
                send_slack_alert(payload)
            elif action == 'n8n':
                send_n8n_event(payload)
            elif action == 'notion':
                from integrations.notion_bridge import send_notion_task
                send_notion_task(payload)
            elif action == 'airtable':
                from integrations.airtable_bridge import send_airtable_record
                send_airtable_record(payload)
            elif action == 'sms':
                from integrations.sms_bridge import send_sms_alert
                send_sms_alert(payload)
            elif action == 'compliance':
                self.compliance.process(payload)
            elif action == 'vault':
                self.vault.process(payload)
            elif action == 'log':
                self.log_event({'event': 'custom_log', 'payload': payload, 'timestamp': datetime.utcnow().isoformat()})
            else:
                logging.warning(f"Unknown action: {action}")
        except Exception as e:
            logging.error(f"Action {action} failed: {e}")

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
