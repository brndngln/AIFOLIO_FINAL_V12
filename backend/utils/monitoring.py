import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VaultMetrics:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 1):
        """
        Initialize metrics tracking
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number for metrics
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self._last_cleanup = datetime.now()
        self._metrics = {
            'cache': [],
            'rate_limit': [],
            'errors': [],
            'performance': [],
            'system': [],
            'user': [],
            'api': []
        }
        
    def track_cache_metrics(self, cache_key: str, hit: bool, response_time: float = None, strategy: str = None) -> None:
        """Track cache hit/miss metrics with strategy information"""
        metrics = {
            "cache_key": cache_key,
            "hit": hit,
            "response_time": response_time,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['cache'].append(metrics)
        self.client.rpush('cache_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_rate_limit_metrics(self, success: bool, error_type: str = None, wait_time: float = None, context: Dict = None) -> None:
        """Track rate limit metrics with context"""
        metrics = {
            "success": success,
            "error_type": error_type,
            "wait_time": wait_time,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['rate_limit'].append(metrics)
        self.client.rpush('rate_limit_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_error_metrics(self, error_type: str, details: Dict, context: Dict = None) -> None:
        """Track error occurrences with context"""
        metrics = {
            "error_type": error_type,
            "details": details,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['errors'].append(metrics)
        self.client.rpush('error_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_performance_metrics(self, operation: str, duration: float, context: Dict = None) -> None:
        """Track performance metrics with context"""
        metrics = {
            "operation": operation,
            "duration": duration,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['performance'].append(metrics)
        self.client.rpush('performance_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_system_metrics(self, memory_usage: float, cpu_load: float, disk_usage: float) -> None:
        """Track system resource metrics"""
        metrics = {
            "memory_usage": memory_usage,
            "cpu_load": cpu_load,
            "disk_usage": disk_usage,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['system'].append(metrics)
        self.client.rpush('system_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_user_metrics(self, user_id: str, action: str, context: Dict = None) -> None:
        """Track user-specific metrics"""
        metrics = {
            "user_id": user_id,
            "action": action,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['user'].append(metrics)
        self.client.rpush('user_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_api_metrics(self, endpoint: str, status_code: int, duration: float, context: Dict = None) -> None:
        """Track API endpoint metrics"""
        metrics = {
            "endpoint": endpoint,
            "status_code": status_code,
            "duration": duration,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        self._metrics['api'].append(metrics)
        self.client.rpush('api_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def get_system_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get system resource metrics"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('system_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        return {
            "average_memory_usage": (
                sum(m['memory_usage'] for m in metrics) / len(metrics)
            ) if metrics else 0,
            "average_cpu_load": (
                sum(m['cpu_load'] for m in metrics) / len(metrics)
            ) if metrics else 0,
            "average_disk_usage": (
                sum(m['disk_usage'] for m in metrics) / len(metrics)
            ) if metrics else 0,
            "timestamp": datetime.now().isoformat()
        }
        
    def get_user_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get user activity metrics"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('user_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        user_actions = {}
        for m in metrics:
            user_id = m['user_id']
            action = m['action']
            if user_id not in user_actions:
                user_actions[user_id] = {}
            if action not in user_actions[user_id]:
                user_actions[user_id][action] = 0
            user_actions[user_id][action] += 1
        
        return {
            "total_users": len(user_actions),
            "user_actions": user_actions,
            "timestamp": datetime.now().isoformat()
        }
        
    def get_api_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get API endpoint metrics"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('api_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        endpoints = {}
        for m in metrics:
            endpoint = m['endpoint']
            status_code = m['status_code']
            if endpoint not in endpoints:
                endpoints[endpoint] = {
                    "total_calls": 0,
                    "success": 0,
                    "failure": 0,
                    "average_duration": 0
                }
            endpoints[endpoint]["total_calls"] += 1
            if status_code < 400:
                endpoints[endpoint]["success"] += 1
            else:
                endpoints[endpoint]["failure"] += 1
            endpoints[endpoint]["average_duration"] += m['duration']
        
        # Calculate average durations
        for endpoint in endpoints:
            if endpoints[endpoint]["total_calls"] > 0:
                endpoints[endpoint]["average_duration"] /= endpoints[endpoint]["total_calls"]
        
        return {
            "endpoints": endpoints,
            "timestamp": datetime.now().isoformat()
        }
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 1):
        """
        Initialize metrics tracking
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number for metrics
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self._last_cleanup = datetime.now()
        
    def track_cache_metrics(self, cache_key: str, hit: bool) -> None:
        """Track cache hit/miss metrics"""
        metrics = {
            "cache_hits": 1 if hit else 0,
            "cache_misses": 0 if hit else 1,
            "timestamp": datetime.now().isoformat()
        }
        
        self.client.rpush('cache_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def track_rate_limit_metrics(self, success: bool, error_type: str = None) -> None:
        """Track rate limit metrics"""
        metrics = {
            "success": success,
            "error_type": error_type,
            "timestamp": datetime.now().isoformat()
        }
        
        self.client.rpush('rate_limit_metrics', json.dumps(metrics))
        self._cleanup_old_metrics()
        
    def get_cache_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get detailed cache metrics for the last X minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('cache_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        # Calculate detailed statistics
        cache_hits = sum(m['cache_hits'] for m in metrics)
        cache_misses = sum(m['cache_misses'] for m in metrics)
        total_requests = len(metrics)
        
        return {
            "total_requests": total_requests,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "cache_hit_rate": (cache_hits / total_requests) if total_requests else 0,
            "cache_miss_rate": (cache_misses / total_requests) if total_requests else 0,
            "average_response_time": self._calculate_average_response_time(metrics),
            "cache_size": self._get_current_cache_size(),
            "cache_keys": self._get_active_cache_keys(),
            "timestamp": datetime.now().isoformat(),
            "metrics_period": f"Last {minutes} minutes",
            "cache_efficiency": self._calculate_cache_efficiency(cache_hits, total_requests)
        }
        
    def _calculate_average_response_time(self, metrics: list) -> float:
        """Calculate average response time from metrics"""
        total_time = sum(m.get('response_time', 0) for m in metrics)
        return total_time / len(metrics) if metrics else 0
        
    def _get_current_cache_size(self) -> int:
        """Get current cache size in bytes"""
        return self.client.info()['used_memory']
        
    def _get_active_cache_keys(self) -> list:
        """Get list of active cache keys"""
        return [key.decode() for key in self.client.keys('vault_*')]
        
    def _calculate_cache_efficiency(self, hits: int, total: int) -> float:
        """Calculate cache efficiency"""
        if total == 0:
            return 0
        return (hits / total) * 100
        
    def get_rate_limit_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get detailed rate limit metrics for the last X minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('rate_limit_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        # Calculate detailed statistics
        total_requests = len(metrics)
        successful_requests = sum(m['success'] for m in metrics)
        
        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": total_requests - successful_requests,
            "success_rate": (successful_requests / total_requests) if total_requests else 0,
            "error_types": {
                "rate_limit": sum(1 for m in metrics if m.get('error_type') == 'rate_limit'),
                "quota": sum(1 for m in metrics if m.get('error_type') == 'quota'),
                "validation": sum(1 for m in metrics if m.get('error_type') == 'validation'),
                "network": sum(1 for m in metrics if m.get('error_type') == 'network'),
                "auth": sum(1 for m in metrics if m.get('error_type') == 'auth')
            },
            "average_retry_count": self._calculate_average_retries(metrics),
            "timestamp": datetime.now().isoformat(),
            "metrics_period": f"Last {minutes} minutes",
            "rate_limit_efficiency": self._calculate_rate_limit_efficiency(successful_requests, total_requests)
        }
        
    def _calculate_average_retries(self, metrics: list) -> float:
        """Calculate average retry count"""
        total_retries = sum(m.get('retry_count', 0) for m in metrics)
        return total_retries / len(metrics) if metrics else 0
        
    def _calculate_rate_limit_efficiency(self, successful: int, total: int) -> float:
        """Calculate rate limit efficiency"""
        if total == 0:
            return 0
        return (successful / total) * 100
        
    def get_rate_limit_metrics(self, minutes: int = 60) -> Dict[str, Any]:
        """Get rate limit metrics for the last X minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        metrics = []
        
        for raw_metric in self.client.lrange('rate_limit_metrics', 0, -1):
            metric = json.loads(raw_metric)
            if datetime.fromisoformat(metric['timestamp']) >= cutoff:
                metrics.append(metric)
        
        return {
            "total_requests": len(metrics),
            "successful_requests": sum(m['success'] for m in metrics),
            "failed_requests": len(metrics) - sum(m['success'] for m in metrics),
            "error_types": {
                "rate_limit": sum(1 for m in metrics if m.get('error_type') == 'rate_limit'),
                "quota": sum(1 for m in metrics if m.get('error_type') == 'quota'),
                "validation": sum(1 for m in metrics if m.get('error_type') == 'validation')
            },
            "timestamp": datetime.now().isoformat()
        }
        
    def _cleanup_old_metrics(self) -> None:
        """Clean up old metrics and optimize Redis memory usage"""
        if datetime.now() - self._last_cleanup > timedelta(hours=24):
            cutoff = datetime.now() - timedelta(hours=24)
            keys_to_cleanup = ['cache_metrics', 'rate_limit_metrics']
            
            for key in keys_to_cleanup:
                while True:
                    raw_metric = self.client.lindex(key, 0)
                    if not raw_metric:
                        break
                    metric = json.loads(raw_metric)
                    if datetime.fromisoformat(metric['timestamp']) < cutoff:
                        self.client.lpop(key)
                    else:
                        break
            
            # Optimize Redis memory
            self.client.memory_purge()
            self._last_cleanup = datetime.now()
        """Clean up old metrics older than 24 hours"""
        if datetime.now() - self._last_cleanup > timedelta(hours=24):
            cutoff = datetime.now() - timedelta(hours=24)
            
            for key in ['cache_metrics', 'rate_limit_metrics']:
                while True:
                    raw_metric = self.client.lindex(key, 0)
                    if not raw_metric:
                        break
                    metric = json.loads(raw_metric)
                    if datetime.fromisoformat(metric['timestamp']) < cutoff:
                        self.client.lpop(key)
                    else:
                        break
            
            self._last_cleanup = datetime.now()
