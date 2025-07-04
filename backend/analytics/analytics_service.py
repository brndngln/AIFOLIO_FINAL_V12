import time
import logging
from typing import Dict, Any
from collections import defaultdict
import json
from redis import Redis

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.metrics = {
            'request_count': 0,
            'error_count': 0,
            'response_time': [],
            'cache_hits': 0,
            'cache_misses': 0,
            'memory_usage': [],
            'conversion_rate': 0.0,
            'user_engagement': defaultdict(int)
        }
        self.start_time = time.time()

    def record_request(self, endpoint: str, response_time: float, success: bool = True):
        """Record a request and its metrics."""
        self.metrics['request_count'] += 1
        self.metrics['response_time'].append(response_time)
        
        if not success:
            self.metrics['error_count'] += 1
            
        # Store metrics in Redis with TTL
        self._store_metric('request_count', self.metrics['request_count'])
        self._store_metric('response_time', response_time)
        self._store_metric('error_count', self.metrics['error_count'])

    def record_cache_hit(self):
        """Record a cache hit."""
        self.metrics['cache_hits'] += 1
        self._store_metric('cache_hits', self.metrics['cache_hits'])

    def record_cache_miss(self):
        """Record a cache miss."""
        self.metrics['cache_misses'] += 1
        self._store_metric('cache_misses', self.metrics['cache_misses'])

    def record_memory_usage(self, usage: int):
        """Record memory usage."""
        self.metrics['memory_usage'].append(usage)
        self._store_metric('memory_usage', usage)

    def record_user_engagement(self, user_id: str, action: str):
        """Record user engagement metrics."""
        key = f"user_engagement:{user_id}:{action}"
        self.redis.incr(key)
        self.redis.expire(key, 86400)  # 24 hours TTL

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics with anomaly detection and explainability."""
        metrics = {
            'request_rate': self._calculate_request_rate(),
            'error_rate': self._calculate_error_rate(),
            'average_response_time': self._calculate_average_response_time(),
            'cache_hit_rate': self._calculate_cache_hit_rate(),
            'memory_usage': self._calculate_average_memory_usage(),
            'user_engagement': self._get_user_engagement(),
            'uptime': self._calculate_uptime()
        }
        anomalies, explanations = self.detect_anomalies(metrics)
        metrics['anomalies'] = anomalies
        metrics['anomaly_explanations'] = explanations
        self._audit_anomalies(anomalies, explanations)
        return metrics

    def detect_anomalies(self, metrics: Dict[str, Any]):
        """Detect anomalies using Z-score and provide explanations."""
        anomalies = {}
        explanations = {}
        # Example: flag error_rate > 10% as anomaly
        if metrics['error_rate'] > 10.0:
            anomalies['error_rate'] = metrics['error_rate']
            explanations['error_rate'] = 'Error rate exceeds 10% threshold.'
        # Example: flag response time anomaly
        avg = metrics['average_response_time']
        if avg > 2.0:
            anomalies['average_response_time'] = avg
            explanations['average_response_time'] = 'Average response time is high (>2s).'
        # Add more as needed
        return anomalies, explanations

    def _audit_anomalies(self, anomalies, explanations):
        if anomalies:
            with open('analytics_anomalies_audit.log', 'a') as f:
                f.write(json.dumps({'timestamp': time.time(), 'anomalies': anomalies, 'explanations': explanations}) + '\n')

    def _store_metric(self, metric_name: str, value: Any):
        """Store metric in Redis with appropriate TTL."""
        key = f"analytics:{metric_name}:{int(time.time())}"
        self.redis.set(key, value)
        self.redis.expire(key, 3600)  # 1 hour TTL

    def _calculate_request_rate(self) -> float:
        """Calculate requests per minute."""
        current_time = time.time()
        return self.metrics['request_count'] / ((current_time - self.start_time) / 60)

    def _calculate_error_rate(self) -> float:
        """Calculate error rate as percentage."""
        if self.metrics['request_count'] == 0:
            return 0.0
        return (self.metrics['error_count'] / self.metrics['request_count']) * 100

    def _calculate_average_response_time(self) -> float:
        """Calculate average response time."""
        if not self.metrics['response_time']:
            return 0.0
        return sum(self.metrics['response_time']) / len(self.metrics['response_time'])

    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate."""
        total = self.metrics['cache_hits'] + self.metrics['cache_misses']
        if total == 0:
            return 0.0
        return (self.metrics['cache_hits'] / total) * 100

    def _calculate_average_memory_usage(self) -> float:
        """Calculate average memory usage."""
        if not self.metrics['memory_usage']:
            return 0.0
        return sum(self.metrics['memory_usage']) / len(self.metrics['memory_usage'])

    def _get_user_engagement(self) -> Dict[str, Any]:
        """Get user engagement metrics."""
        engagement = {}
        for key in self.redis.scan_iter("user_engagement:*"):
            parts = key.decode().split(':')
            user_id = parts[1]
            action = parts[2]
            count = int(self.redis.get(key))
            
            if user_id not in engagement:
                engagement[user_id] = {}
            
            engagement[user_id][action] = count
        
        return engagement

    def _calculate_uptime(self) -> float:
        """Calculate system uptime in minutes."""
        return (time.time() - self.start_time) / 60

    def get_realtime_metrics(self) -> Dict[str, Any]:
        """Get real-time metrics for monitoring."""
        return {
            'request_count': self.metrics['request_count'],
            'error_count': self.metrics['error_count'],
            'cache_hits': self.metrics['cache_hits'],
            'cache_misses': self.metrics['cache_misses'],
            'memory_usage': self.metrics['memory_usage'][-1] if self.metrics['memory_usage'] else 0
        }
