import time
import json
from typing import Dict, Any, Optional, Callable, Union
from redis import Redis
import logging
from functools import wraps

logger = logging.getLogger(__name__)


class CacheService:
    def __init__(self, redis_client: Redis, default_ttl: int = 3600):
        self.redis = redis_client
        self.default_ttl = default_ttl
        self.cache_hits = 0
        self.cache_misses = 0

    def cache(
        self,
        key: Union[str, Callable],
        ttl: Optional[int] = None,
        cache_by: Optional[str] = None,
        cache_on_error: bool = False,
    ):
        """
        Cache decorator that caches function results.

        Args:
            key: Either a string key or a function that generates a key
            ttl: Time-to-live in seconds
            cache_by: Optional parameter name to use for cache key
            cache_on_error: Whether to cache error results
        """
        if ttl is None:
            ttl = self.default_ttl

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                if callable(key):
                    cache_key = key(*args, **kwargs)
                elif cache_by and cache_by in kwargs:
                    cache_key = f"{func.__name__}:{kwargs[cache_by]}"
                else:
                    cache_key = f"{func.__name__}:{key}"

                # Try to get from cache
                cached = self.redis.get(cache_key)
                if cached is not None:
                    self.cache_hits += 1
                    return json.loads(cached)

                self.cache_misses += 1

                try:
                    # Call the function
                    result = await func(*args, **kwargs)

                    # Cache the result
                    self.redis.set(cache_key, json.dumps(result))
                    self.redis.expire(cache_key, ttl)

                    return result

                except Exception as e:
                    if cache_on_error:
                        self.redis.set(
                            cache_key,
                            json.dumps({"error": str(e), "timestamp": time.time()}),
                        )
                        self.redis.expire(cache_key, ttl)
                    raise

            return wrapper

        return decorator

    def cache_batch(self, key_prefix: str, ttl: Optional[int] = None):
        """
        Cache decorator for batch operations.

        Args:
            key_prefix: Prefix for cache keys
            ttl: Time-to-live in seconds
        """
        if ttl is None:
            ttl = self.default_ttl

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Try to get all keys from cache
                keys = kwargs.get("keys", [])
                cache_keys = [f"{key_prefix}:{key}" for key in keys]
                cached_results = self.redis.mget(cache_keys)

                # Separate cached and uncached results
                cached = {}
                uncached = []

                for key, result in zip(keys, cached_results):
                    if result is not None:
                        cached[key] = json.loads(result)
                    else:
                        uncached.append(key)

                # If all results are cached, return them
                if not uncached:
                    return cached

                # Call the function for uncached results
                new_results = await func(*args, **{**kwargs, "keys": uncached})

                # Cache new results
                for key, result in new_results.items():
                    cache_key = f"{key_prefix}:{key}"
                    self.redis.set(cache_key, json.dumps(result))
                    self.redis.expire(cache_key, ttl)

                # Combine cached and new results
                return {**cached, **new_results}

            return wrapper

        return decorator

    def cache_warm(self, func: Callable, *args, **kwargs):
        """Warm up the cache by pre-fetching results."""
        result = func(*args, **kwargs)
        key = f"{func.__name__}:{args[0] if args else kwargs.get('key', '')}"
        self.redis.set(key, json.dumps(result))
        self.redis.expire(key, self.default_ttl)
        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Get cache metrics."""
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_rate": (self.cache_hits / (self.cache_hits + self.cache_misses))
            if (self.cache_hits + self.cache_misses) > 0
            else 0,
            "total_keys": len(self.redis.keys("cache:*")),
        }

    def clear_cache(self, pattern: str = "*"):
        """Clear cache entries matching pattern."""
        keys = self.redis.keys(f"cache:{pattern}")
        if keys:
            self.redis.delete(*keys)
            return len(keys)
        return 0
