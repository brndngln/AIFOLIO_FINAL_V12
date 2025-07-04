import threading
import time
import json
import os
from collections import defaultdict, deque

_METRICS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/hook_metrics.json'))
_LOCK = threading.Lock()

class HookMetrics:
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            'success': 0,
            'failure': 0,
            'total_time': 0.0,
            'anomaly': 0,
            'fraud': 0,
            'compliance': 0,
            'errors': deque(maxlen=20)
        })
        self.load()

    def record(self, hook, success, elapsed, anomaly=False, fraud=False, compliance=False, error=None):
        with _LOCK:
            m = self.metrics[hook]
            if success:
                m['success'] += 1
            else:
                m['failure'] += 1
            m['total_time'] += elapsed
            if anomaly:
                m['anomaly'] += 1
            if fraud:
                m['fraud'] += 1
            if compliance:
                m['compliance'] += 1
            if error:
                m['errors'].appendleft({'time': time.time(), 'error': error})
            self.save()

    def get_metrics(self):
        with _LOCK:
            summary = {}
            for hook, m in self.metrics.items():
                total = m['success'] + m['failure']
                avg_time = m['total_time'] / total if total else 0.0
                summary[hook] = {
                    'success': m['success'],
                    'failure': m['failure'],
                    'avg_time': avg_time,
                    'anomaly': m['anomaly'],
                    'fraud': m['fraud'],
                    'compliance': m['compliance'],
                    'recent_errors': list(m['errors'])
                }
            return summary

    def save(self):
        try:
            with open(_METRICS_PATH, 'w') as f:
                json.dump(self.get_metrics(), f, indent=2)
        except Exception:
            pass

    def load(self):
        if os.path.exists(_METRICS_PATH):
            try:
                with open(_METRICS_PATH, 'r') as f:
                    data = json.load(f)
                    for hook, m in data.items():
                        self.metrics[hook].update(m)
                        self.metrics[hook]['errors'] = deque(m.get('recent_errors', []), maxlen=20)
            except Exception:
                pass

hook_metrics = HookMetrics()
