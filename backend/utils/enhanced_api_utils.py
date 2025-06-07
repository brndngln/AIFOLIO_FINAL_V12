from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Dict, TypeVar, ParamSpec, Type
import json
import os
import logging
import time
import random
import redis
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAIError
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Type variables for better type hints
T = TypeVar('T')
P = ParamSpec('P')

class APIError(Exception):
    """Base class for API-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.details = details or {}

class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "allowed_calls": 60,
            "time_window": "1 minute",
            "suggested_wait": "60 seconds"
        }

class QuotaError(APIError):
    """Raised when API quota is exceeded"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "plan": "Standard",
            "current_usage": 0,
            "max_allowed": 1000,
            "reset_time": "24 hours"
        }

class ValidationError(APIError):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "required_fields": [
                "topic",
                "description",
                "chapters",
                "cta"
            ],
            "validation_rules": {
                "title": "10-100 characters",
                "description": "50-500 characters",
                "chapters": "Minimum 3 chapters",
                "cta": "10-200 characters"
            }
        }

class NetworkError(APIError):
    """Raised when network connection fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "connection_type": "API",
            "retry_possible": True,
            "suggested_actions": [
                "Check internet connection",
                "Verify API endpoint",
                "Try again later"
            ]
        }

class AuthenticationError(APIError):
    """Raised when authentication fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "auth_type": "API Key",
            "required_fields": ["api_key"],
            "suggested_actions": [
                "Check API key validity",
                "Verify permissions",
                "Contact support"
            ]
        }

class CacheError(APIError):
    """Raised when cache operations fail"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "cache_type": "Redis",
            "operation": "Unknown",
            "suggested_actions": [
                "Check Redis connection",
                "Verify cache key",
                "Clear cache"
            ]
        }

class ConfigurationError(APIError):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "required_config": [],
            "suggested_actions": [
                "Check environment variables",
                "Verify config file",
                "Contact administrator"
            ]
        }

class TimeoutError(APIError):
    """Raised when operation times out"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "timeout_seconds": 30,
            "operation": "Unknown",
            "suggested_actions": [
                "Increase timeout",
                "Check network",
                "Retry with exponential backoff"
            ]
        }

class ResourceLimitError(APIError):
    """Raised when resource limits are exceeded"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "resource_type": "Unknown",
            "current_usage": 0,
            "max_allowed": 0,
            "suggested_actions": [
                "Upgrade plan",
                "Optimize usage",
                "Contact support"
            ]
        }

class ServiceUnavailableError(APIError):
    """Raised when service is unavailable"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "service": "Unknown",
            "status": "Down",
            "suggested_actions": [
                "Check service status",
                "Retry later",
                "Contact support"
            ]
        }

class PermissionError(APIError):
    """Raised when permissions are insufficient"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "required_permissions": [],
            "current_permissions": [],
            "suggested_actions": [
                "Request elevated permissions",
                "Verify role",
                "Contact administrator"
            ]
        }
    """Base class for API-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message)
        self.details = details or {}

class RateLimitError(APIError):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "allowed_calls": 60,
            "time_window": "1 minute",
            "suggested_wait": "60 seconds"
        }

class QuotaError(APIError):
    """Raised when API quota is exceeded"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "plan": "Standard",
            "current_usage": 0,
            "max_allowed": 1000,
            "reset_time": "24 hours"
        }

class ValidationError(APIError):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "required_fields": [
                "topic",
                "description",
                "chapters",
                "cta"
            ],
            "validation_rules": {
                "title": "10-100 characters",
                "description": "50-500 characters",
                "chapters": "Minimum 3 chapters",
                "cta": "10-200 characters"
            }
        }

class NetworkError(APIError):
    """Raised when network connection fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "connection_type": "API",
            "retry_possible": True,
            "suggested_actions": [
                "Check internet connection",
                "Verify API endpoint",
                "Try again later"
            ]
        }

class AuthenticationError(APIError):
    """Raised when authentication fails"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(message, details)
        self.details = details or {
            "auth_type": "API Key",
            "required_fields": ["api_key"],
            "suggested_actions": [
                "Check API key validity",
                "Verify permissions",
                "Contact support"
            ]
        }

class CacheStrategy:
    def __init__(self, name: str, ttl: int, max_size: int):
        """
        Base cache strategy class
        
        Args:
            name: Strategy name
            ttl: Time-to-live in seconds
            max_size: Maximum number of items
        """
        self.name = name
        self.ttl = ttl
        self.max_size = max_size

    def should_cache(self, key: str, value: Any) -> bool:
        """Determine if item should be cached"""
        return True

    def get_cache_key(self, key: str) -> str:
        """Generate cache key with strategy prefix"""
        return f"{self.name}:{key}"

    def cleanup(self) -> None:
        """Cleanup expired items"""
        pass

class TimeBasedStrategy(CacheStrategy):
    def __init__(self, ttl: int = 3600, max_size: int = 100):
        """
        Time-based caching strategy
        
        Args:
            ttl: Time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of items (default: 100)
        """
        super().__init__('time_based', ttl, max_size)

class FrequencyBasedStrategy(CacheStrategy):
    def __init__(self, min_hits: int = 5, ttl: int = 86400, max_size: int = 50):
        """
        Frequency-based caching strategy
        
        Args:
            min_hits: Minimum number of hits to cache
            ttl: Time-to-live in seconds (default: 24 hours)
            max_size: Maximum number of items (default: 50)
        """
        super().__init__('frequency_based', ttl, max_size)
        self.min_hits = min_hits
        self.hit_counter = {}

class LRUStrategy(CacheStrategy):
    def __init__(self, ttl: int = 3600, max_size: int = 100, eviction_threshold: float = 0.8):
        """
        Least Recently Used caching strategy
        
        Args:
            ttl: Time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of items (default: 100)
            eviction_threshold: Percentage of max size to trigger eviction (default: 80%)
        """
        super().__init__('lru', ttl, max_size)
        self.eviction_threshold = eviction_threshold
        self.access_times = {}
        self.size = 0

    def should_cache(self, key: str, value: Any) -> bool:
        """Determine if item should be cached based on size"""
        item_size = len(json.dumps(value))
        if self.size + item_size > self.max_size:
            self._evict_items()
        return True

    def _evict_items(self) -> None:
        """Evict least recently used items"""
        sorted_items = sorted(
            self.access_times.items(),
            key=lambda x: x[1]
        )
        
        while self.size > self.max_size * self.eviction_threshold:
            key = sorted_items.pop(0)[0]
            self.size -= len(json.dumps(self.client.get(self.get_cache_key(key))))
            self.client.delete(self.get_cache_key(key))
            del self.access_times[key]

    def get_cache_key(self, key: str) -> str:
        """Generate cache key with strategy prefix"""
        cache_key = super().get_cache_key(key)
        self.access_times[key] = time.time()
        return cache_key

class ContentBasedStrategy(CacheStrategy):
    def __init__(self, similarity_threshold: float = 0.8, ttl: int = 3600, max_size: int = 100):
        """
        Content-based caching strategy
        
        Args:
            similarity_threshold: Minimum similarity score to use cached content
            ttl: Time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of items (default: 100)
        """
        super().__init__('content_based', ttl, max_size)
        self.similarity_threshold = similarity_threshold
        self.content_hashes = {}

    def _calculate_similarity(self, content1: str, content2: str) -> float:
        """Calculate similarity between two pieces of content"""
        # Simple implementation using Jaccard similarity
        set1 = set(content1.lower().split())
        set2 = set(content2.lower().split())
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union) if union else 0

    def should_cache(self, key: str, value: Any) -> bool:
        """Determine if item should be cached based on content similarity"""
        if isinstance(value, str):
            for existing_key, existing_hash in self.content_hashes.items():
                similarity = self._calculate_similarity(value, existing_hash)
                if similarity >= self.similarity_threshold:
                    return False
            self.content_hashes[key] = value
        return True

class ContextualStrategy(CacheStrategy):
    def __init__(self, context_fields: list = None, ttl: int = 3600, max_size: int = 100):
        """
        Contextual caching strategy
        
        Args:
            context_fields: List of fields to consider for context
            ttl: Time-to-live in seconds (default: 1 hour)
            max_size: Maximum number of items (default: 100)
        """
        super().__init__('contextual', ttl, max_size)
        self.context_fields = context_fields or ['topic', 'language', 'version']
        self.context_cache = {}

    def get_cache_key(self, key: str) -> str:
        """Generate context-aware cache key"""
        # Extract context from key
        context = {}
        for field in self.context_fields:
            if field in key:
                context[field] = key.split(field)[-1].split('_')[0]
        
        context_key = '_'.join(f"{k}_{v}" for k, v in sorted(context.items()))
        return f"{self.name}:{context_key}:{key}"
        """
        Frequency-based caching strategy
        
        Args:
            min_hits: Minimum number of hits to cache
            ttl: Time-to-live in seconds (default: 24 hours)
            max_size: Maximum number of items (default: 50)
        """
        super().__init__('frequency_based', ttl, max_size)
        self.min_hits = min_hits
        self.hit_counter = {}

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        Initialize Redis cache with multiple strategies
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self._last_cleanup = datetime.now()
        self.strategies = {
            'time_based': TimeBasedStrategy(),
            'frequency_based': FrequencyBasedStrategy(),
            'lru': LRUStrategy(),
            'content_based': ContentBasedStrategy(),
            'contextual': ContextualStrategy()
        }
        self.strategy_order = [
            'contextual',  # First, try contextual caching
            'content_based',  # Then check content similarity
            'frequency_based',  # Next, check frequency
            'lru',  # Then use LRU
            'time_based'  # Finally, fall back to time-based
        ]

    def get(self, key: str, context: Optional[Dict] = None) -> Optional[Any]:
        """
        Get cached item with intelligent strategy selection
        
        Args:
            key: Cache key
            context: Optional context information for contextual caching
        """
        for strategy_name in self.strategy_order:
            strategy = self.strategies[strategy_name]
            if strategy_name == 'contextual' and context:
                # For contextual strategy, use the provided context
                cache_key = strategy.get_cache_key(key)
            else:
                cache_key = strategy.get_cache_key(key)
            
            try:
                data = self.client.get(cache_key)
                if data:
                    self._increment_hit_counter(key)
                    return json.loads(data)
            except redis.RedisError as e:
                logger.error(f"Redis error while getting: {str(e)}")
                continue
        return None

    def set(self, key: str, value: Any, context: Optional[Dict] = None) -> None:
        """
        Set cached item with intelligent strategy selection
        
        Args:
            key: Cache key
            value: Value to cache
            context: Optional context information for contextual caching
        """
        for strategy_name in self.strategy_order:
            strategy = self.strategies[strategy_name]
            if not strategy.should_cache(key, value):
                continue
                
            if strategy_name == 'contextual' and context:
                cache_key = strategy.get_cache_key(key)
            else:
                cache_key = strategy.get_cache_key(key)
            
            try:
                self.client.setex(
                    cache_key,
                    strategy.ttl,
                    json.dumps(value)
                )
                logger.info(f"Cached {key} with {strategy_name} strategy")
                break  # Stop after first successful cache
            except redis.RedisError as e:
                logger.error(f"Redis error while setting: {str(e)}")
                continue

    def get_strategy_stats(self) -> Dict[str, Any]:
        """Get statistics about cache usage per strategy"""
        stats = {}
        for name, strategy in self.strategies.items():
            stats[name] = {
                "hits": sum(1 for k in self.client.scan_iter(f"{name}:*") if self.client.get(k)),
                "misses": sum(1 for k in self.client.scan_iter(f"{name}:*") if not self.client.get(k)),
                "size": sum(len(v) for v in self.client.mget(self.client.scan_iter(f"{name}:*")) if v),
                "ttl": strategy.ttl
            }
        return stats

    def optimize_cache(self) -> None:
        """Optimize cache usage across all strategies"""
        # Get current stats
        stats = self.get_strategy_stats()
        
        # Analyze usage patterns
        for name, strategy in self.strategies.items():
            strategy_stats = stats[name]
            hit_rate = (strategy_stats['hits'] / 
                         (strategy_stats['hits'] + strategy_stats['misses']))
            success_rate = (strategy_stats['hits'] / (strategy_stats['hits'] + strategy_stats['misses'])) if (strategy_stats['hits'] + strategy_stats['misses']) > 0 else 0
            
            # Adjust TTL based on hit rate
            if hit_rate < 0.2:  # Low hit rate
                strategy.ttl = max(60, strategy.ttl * 0.9)  # Decrease TTL
            elif hit_rate > 0.8:  # High hit rate
                strategy.ttl = min(86400, strategy.ttl * 1.1)  # Increase TTL
            
            # Log optimization
            logger.info(f"Optimizing {name} strategy - "
                       f"Hit rate: {hit_rate:.2f}, "
                       f"New TTL: {strategy.ttl} seconds")

    def cleanup(self) -> None:
        """Clean up expired items and optimize cache"""
        super().cleanup()
        self.optimize_cache()
        """
        Initialize Redis cache with multiple strategies
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        self._last_cleanup = datetime.now()
        self.strategies = {
            'time_based': TimeBasedStrategy(),
            'frequency_based': FrequencyBasedStrategy()
        }

    def get(self, key: str, strategy: str = 'time_based') -> Optional[Any]:
        """
        Get cached item with specified strategy
        
        Args:
            key: Cache key
            strategy: Caching strategy to use
        """
        if strategy not in self.strategies:
            raise ValueError(f"Invalid strategy: {strategy}")
            
        cache_key = self.strategies[strategy].get_cache_key(key)
        try:
            data = self.client.get(cache_key)
            if data:
                self._increment_hit_counter(key)
                return json.loads(data)
            return None
        except redis.RedisError as e:
            logger.error(f"Redis error while getting: {str(e)}")
            return None

    def set(self, key: str, value: Any, strategy: str = 'time_based') -> None:
        """
        Set cached item with specified strategy
        
        Args:
            key: Cache key
            value: Value to cache
            strategy: Caching strategy to use
        """
        if strategy not in self.strategies:
            raise ValueError(f"Invalid strategy: {strategy}")
            
        if not self.strategies[strategy].should_cache(key, value):
            return
            
        cache_key = self.strategies[strategy].get_cache_key(key)
        try:
            self.client.setex(
                cache_key,
                self.strategies[strategy].ttl,
                json.dumps(value)
            )
            logger.info(f"Cached {key} with {strategy} strategy")
        except redis.RedisError as e:
            logger.error(f"Redis error while setting: {str(e)}")

    def _increment_hit_counter(self, key: str) -> None:
        """Increment hit counter for frequency-based caching"""
        freq_strategy = self.strategies['frequency_based']
        if key not in freq_strategy.hit_counter:
            freq_strategy.hit_counter[key] = 0
        freq_strategy.hit_counter[key] += 1

    def clear(self, strategy: str = None) -> None:
        """
        Clear cache for specified strategy
        
        Args:
            strategy: Strategy to clear (None for all)
        """
        try:
            if strategy:
                if strategy not in self.strategies:
                    raise ValueError(f"Invalid strategy: {strategy}")
                pattern = f"{strategy}:*"
            else:
                pattern = "*"
                
            for key in self.client.scan_iter(pattern):
                self.client.delete(key)
            logger.info(f"Redis cache cleared for {strategy or 'all'}")
        except redis.RedisError as e:
            logger.error(f"Redis error while clearing: {str(e)}")

    def cleanup(self) -> None:
        """Clean up expired items for all strategies"""
        for strategy in self.strategies.values():
            strategy.cleanup()
            self._cleanup_expired_items(strategy)

    def _cleanup_expired_items(self, strategy: CacheStrategy) -> None:
        """Clean up expired items for a specific strategy"""
        pattern = f"{strategy.name}:*"
        for key in self.client.scan_iter(pattern):
            ttl = self.client.ttl(key)
            if ttl == -2:  # Key does not exist
                self.client.delete(key)
                continue
            if ttl == -1:  # No expire set
                self.client.expire(key, strategy.ttl)
        
    def get(self, key: str) -> Optional[Any]:
        """Get cached item from Redis"""
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except redis.RedisError as e:
            logger.error(f"Redis error while getting: {str(e)}")
            return None
            
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set cached item in Redis with TTL"""
        try:
            self.client.setex(key, ttl, json.dumps(value))
            logger.info(f"Cached {key} with TTL: {ttl} seconds")
        except redis.RedisError as e:
            logger.error(f"Redis error while setting: {str(e)}")
            
    def clear(self) -> None:
        """Clear all cached items"""
        try:
            self.client.flushdb()
            logger.info("Redis cache cleared")
        except redis.RedisError as e:
            logger.error(f"Redis error while clearing: {str(e)}")

def cache_vault(topic: str) -> str:
    """Generate a cache key for a vault topic"""
    return f"vault_{topic.lower().replace(' ', '_')}"

def cache_response(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to cache vault generation responses using Redis"""
    cache = RedisCache()
    
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Generate cache key based on function arguments
        cache_key = cache_vault(kwargs.get('topic', 'default'))
        
        # Try to get from cache first
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Redis cache hit for topic: {kwargs.get('topic', 'default')}")
            return cached_result
            
        # If not in cache, call the function
        result = func(*args, **kwargs)
        
        # Store result in cache
        cache.set(cache_key, result)
        logger.info(f"Redis cache miss for topic: {kwargs.get('topic', 'default')}")
        
        return result
    
    return wrapper

def retry_on_api_error(
    attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator that retries API calls with exponential backoff
    
    Args:
        attempts: Maximum number of retry attempts
        base_delay: Base delay in seconds (exponential backoff starts from this)
        max_delay: Maximum delay in seconds
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @retry(
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=base_delay, max=max_delay),
            retry=(retry_if_exception_type(OpenAIError) |
                   retry_if_exception_type(RateLimitError) |
                   retry_if_exception_type(QuotaError) |
                   retry_if_exception_type(ValidationError)),
            reraise=True
        )
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except OpenAIError as e:
                if "rate limit" in str(e).lower():
                    raise RateLimitError(f"Rate limit exceeded: {str(e)}") from e
                elif "quota" in str(e).lower():
                    raise QuotaError(f"Quota exceeded: {str(e)}") from e
                elif "invalid" in str(e).lower():
                    raise ValidationError(f"Invalid input: {str(e)}") from e
                raise
        return wrapper
    return decorator

class RateLimitConfig:
    def __init__(
        self,
        calls_per_minute: int = 60,
        window_size: int = 60,
        max_burst: int = 5,
        burst_window: int = 10,
        grace_period: int = 300,
        cooldown_period: int = 600,
        max_retry_attempts: int = 3,
        ip_based: bool = False,
        user_based: bool = False,
        api_key_based: bool = False,
        region_based: bool = False,
        priority_levels: Dict[str, int] = None,
        burst_factor: float = 1.5,
        adaptive_window: bool = True,
        max_queue_size: int = 100,
        queue_timeout: int = 300
    ):
        """
        Rate limiting configuration
        
        Args:
            calls_per_minute: Maximum calls per minute
            window_size: Size of the time window in seconds
            max_burst: Maximum number of calls in a burst
            burst_window: Time window for burst calculation (seconds)
            grace_period: Initial grace period before strict rate limiting (seconds)
            cooldown_period: Time to wait after rate limit is hit (seconds)
            max_retry_attempts: Maximum retry attempts before failing
            ip_based: Enable IP-based rate limiting
            user_based: Enable user-based rate limiting
            api_key_based: Enable API key-based rate limiting
            region_based: Enable region-based rate limiting
            priority_levels: Dictionary mapping user types to priority levels
            burst_factor: Factor to multiply burst limit by during peak times
            adaptive_window: Enable adaptive window sizing based on load
            max_queue_size: Maximum size of request queue
            queue_timeout: Maximum time a request can wait in queue
        """
        self.calls_per_minute = calls_per_minute
        self.window_size = window_size
        self.max_burst = max_burst
        self.burst_window = burst_window
        self.grace_period = grace_period
        self.cooldown_period = cooldown_period
        self.max_retry_attempts = max_retry_attempts
        self.ip_based = ip_based
        self.user_based = user_based
        self.api_key_based = api_key_based
        self.region_based = region_based
        self.priority_levels = priority_levels or {
            'free': 1,
            'standard': 2,
            'premium': 3,
            'enterprise': 4
        }
        self.burst_factor = burst_factor
        self.adaptive_window = adaptive_window
        self.max_queue_size = max_queue_size
        self.queue_timeout = queue_timeout
        self._last_reset = datetime.now()
        self._current_calls = 0
        self._in_grace_period = True
        self._queue = []
        self._queue_lock = threading.Lock()

    def check_rate_limit(self, context: Dict = None) -> bool:
        """Check if rate limit is exceeded with context"""
        current_time = datetime.now()
        
        # Check if we're in grace period
        if self._in_grace_period:
            if (current_time - self._last_reset).total_seconds() > self.grace_period:
                self._in_grace_period = False
                self._current_calls = 0
            return False
        
        # Apply priority-based rate limiting
        priority = self._get_priority(context)
        if priority:
            self.calls_per_minute = self._adjust_limit_by_priority(
                self.calls_per_minute, priority
            )
            self.max_burst = self._adjust_limit_by_priority(
                self.max_burst, priority
            )
        
        # Check burst limit with adaptive window
        if self.adaptive_window:
            self._adjust_window_size()
        
        # Check regular rate limit
        if self._current_calls >= self.calls_per_minute:
            return True
            
        return False

    def _get_priority(self, context: Dict) -> int:
        """Get user's priority level"""
        if not context:
            return None
        
        if 'user_type' in context:
            return self.priority_levels.get(context['user_type'])
        return None

    def _adjust_limit_by_priority(self, limit: int, priority: int) -> int:
        """Adjust rate limit based on priority"""
        if not priority:
            return limit
            
        # Higher priority means higher limits
        return limit * (priority / max(self.priority_levels.values()))

    def _adjust_window_size(self) -> None:
        """Adjust window size based on system load"""
        # Get current system load (simplified)
        load = self._get_system_load()
        
        # Adjust window size
        if load > 0.8:  # High load
            self.window_size = max(60, self.window_size * 0.9)
        elif load < 0.2:  # Low load
            self.window_size = min(3600, self.window_size * 1.1)

    def _get_system_load(self) -> float:
        """Get system load (simplified)"""
        # This is a placeholder - in production, you'd get real system metrics
        return random.uniform(0.1, 0.9)

    def queue_request(self, request: Any) -> bool:
        """Queue a request if rate limit is hit"""
        with self._queue_lock:
            if len(self._queue) >= self.max_queue_size:
                return False
            self._queue.append((datetime.now(), request))
            return True

    def process_queued_requests(self) -> None:
        """Process queued requests"""
        with self._queue_lock:
            current_time = datetime.now()
            queue = []
            
            # Remove expired requests
            for timestamp, request in self._queue:
                if (current_time - timestamp).total_seconds() < self.queue_timeout:
                    queue.append((timestamp, request))
            
            self._queue = queue
            
            # Process requests that can be handled now
            for timestamp, request in queue:
                if not self.check_rate_limit():
                    self._current_calls += 1
                    # Process the request
                    self._process_request(request)

    def _process_request(self, request: Any) -> None:
        """Process a single request"""
        # This is a placeholder - implement actual request processing
        pass

    def reset(self) -> None:
        """Reset rate limit counters and queue"""
        self._current_calls = 0
        self._last_reset = datetime.now()
        self._in_grace_period = True
        with self._queue_lock:
            self._queue = []
    def __init__(
        self,
        calls_per_minute: int = 60,
        window_size: int = 60,
        max_burst: int = 5,
        burst_window: int = 10,
        grace_period: int = 300,
        cooldown_period: int = 600,
        max_retry_attempts: int = 3
    ):
        """
        Rate limiting configuration
        
        Args:
            calls_per_minute: Maximum calls per minute
            window_size: Size of the time window in seconds
            max_burst: Maximum number of calls in a burst
            burst_window: Time window for burst calculation (seconds)
            grace_period: Initial grace period before strict rate limiting (seconds)
            cooldown_period: Time to wait after rate limit is hit (seconds)
            max_retry_attempts: Maximum retry attempts before failing
        """
        self.calls_per_minute = calls_per_minute
        self.window_size = window_size
        self.max_burst = max_burst
        self.burst_window = burst_window
        self.grace_period = grace_period
        self.cooldown_period = cooldown_period
        self.max_retry_attempts = max_retry_attempts
        self._last_reset = datetime.now()
        self._current_calls = 0
        self._in_grace_period = True

    def check_rate_limit(self) -> bool:
        """Check if rate limit is exceeded"""
        current_time = datetime.now()
        
        # Check if we're in grace period
        if self._in_grace_period:
            if (current_time - self._last_reset).total_seconds() > self.grace_period:
                self._in_grace_period = False
                self._current_calls = 0
            return False
        
        # Check burst limit
        if self._current_calls >= self.max_burst:
            return True
            
        # Check regular rate limit
        if self._current_calls >= self.calls_per_minute:
            return True
            
        return False

    def increment_call(self) -> None:
        """Increment call counter"""
        self._current_calls += 1
        
    def reset(self) -> None:
        """Reset rate limit counters"""
        self._current_calls = 0
        self._last_reset = datetime.now()
        self._in_grace_period = True

def rate_limit(
    calls_per_minute: int = 60,
    window_size: int = 60,
    max_burst: int = 5,
    burst_window: int = 10,
    grace_period: int = 300,
    cooldown_period: int = 600,
    max_retry_attempts: int = 3
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator that implements rate limiting with burst support and configurable parameters
    
    Args:
        calls_per_minute: Maximum number of calls per minute
        window_size: Size of the time window in seconds
        max_burst: Maximum number of calls allowed in a burst
        burst_window: Time window for burst calculation (seconds)
        grace_period: Initial grace period before strict rate limiting (seconds)
        cooldown_period: Time to wait after rate limit is hit (seconds)
        max_retry_attempts: Maximum retry attempts before failing
    """
    class RateLimiter:
        def __init__(self, config: RateLimitConfig):
            self.config = config
            self.calls = []
            self.burst_counter = 0
            self.last_rate_limit = None
            
        def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                current_time = time.time()
                
                # Clean up old calls
                self.calls = [call for call in self.calls 
                             if current_time - call < self.config.window_size]
                
                # Check rate limit
                if self.config.check_rate_limit():
                    if self.last_rate_limit:
                        if (current_time - self.last_rate_limit) < self.config.cooldown_period:
                            raise RateLimitError(
                                f"Rate limit exceeded. Please wait {self.config.cooldown_period} seconds before trying again."
                            )
                    else:
                        self.last_rate_limit = current_time
                        raise RateLimitError(
                            f"Rate limit exceeded. Please wait {self.config.cooldown_period} seconds before trying again."
                        )
                
                # Handle burst
                if self.burst_counter >= self.config.max_burst:
                    time.sleep(random.uniform(0, 0.5))  # Small random delay after burst
                    self.burst_counter = 0
                else:
                    self.burst_counter += 1
                
                # Record the call
                self.calls.append(current_time)
                self.config.increment_call()
                
                # Add a small random delay to prevent thundering herd
                time.sleep(random.uniform(0, 0.5))
                
                # Track metrics
                metrics.track_rate_limit_metrics(
                    success=True,
                    wait_time=time.time() - current_time
                )
                
                return func(*args, **kwargs)
            return wrapper
    
    return RateLimiter(RateLimitConfig(
        calls_per_minute=calls_per_minute,
        window_size=window_size,
        max_burst=max_burst,
        burst_window=burst_window,
        grace_period=grace_period,
        cooldown_period=cooldown_period,
        max_retry_attempts=max_retry_attempts
    ))
    """
    Decorator that implements rate limiting with burst support
    
    Args:
        calls_per_minute: Maximum number of calls per minute
        window_size: Size of the time window in seconds
        max_burst: Maximum number of calls allowed in a burst
    """
    class RateLimiter:
        def __init__(self, calls_per_minute: int, window_size: int, max_burst: int):
            self.calls_per_minute = calls_per_minute
            self.window_size = window_size
            self.max_burst = max_burst
            self.calls = []
            self.burst_counter = 0
            
        def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                # Clean up old calls
                current_time = time.time()
                self.calls = [call for call in self.calls 
                             if current_time - call < self.window_size]
                
                # Check if we can make another call
                if len(self.calls) >= self.calls_per_minute:
                    raise RateLimitError(
                        f"Rate limit exceeded: {self.calls_per_minute} calls per minute"
                    )
                
                # Handle burst
                if self.burst_counter >= self.max_burst:
                    time.sleep(1)  # Small pause after burst
                    self.burst_counter = 0
                else:
                    self.burst_counter += 1
                
                # Record the call
                self.calls.append(current_time)
                
                # Add a small random delay to prevent thundering herd
                time.sleep(random.uniform(0, 0.5))
                
                return func(*args, **kwargs)
            return wrapper
    
    return RateLimiter(calls_per_minute, window_size, max_burst)

def handle_api_errors(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator that handles API-related errors and provides user-friendly messages
    """
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except RateLimitError as e:
            logger.error(f"Rate limit error: {str(e)}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limit",
                    "message": "Too many requests. Please try again later.",
                    "details": str(e),
                    "retry_after": 60,
                    "rate_limit": {
                        "calls_per_minute": 60,
                        "current_calls": len(getattr(wrapper, "calls", []))
                    }
                }
            )
        except QuotaError as e:
            logger.error(f"Quota error: {str(e)}")
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "quota_exceeded",
                    "message": "API quota exceeded. Please upgrade your plan.",
                    "details": str(e),
                    "suggested_actions": [
                        "Upgrade your API plan",
                        "Check your billing details",
                        "Contact support"
                    ]
                }
            )
        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "validation_error",
                    "message": "Invalid input provided.",
                    "details": str(e),
                    "validation_errors": [
                        "Check your input parameters",
                        "Ensure all required fields are present",
                        "Verify data types"
                    ]
                }
            )
        except OpenAIError as e:
            logger.error(f"OpenAI error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "api_error",
                    "message": "Failed to generate vault. Please try again later.",
                    "details": str(e),
                    "error_type": type(e).__name__
                }
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "internal_error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "details": str(e),
                    "error_type": type(e).__name__
                }
            )
    return wrapper
