from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging
from .analytics_service import AnalyticsService
from redis import Redis

logger = logging.getLogger(__name__)


class AnalyticsMiddleware(BaseHTTPMiddleware):
    """
    SAFE AI-compliant: Static analytics middleware. Deterministic, owner-controlled, no adaptive logic.
    """
    def __init__(self, app: object, redis_client: Redis) -> None:
        super().__init__(app)
        self.analytics_service: AnalyticsService = AnalyticsService(redis_client)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        start_time: float = time.time()

        # Record request
        self.analytics_service.record_request(
            endpoint=request.url.path,
            response_time=0.0,  # Will be updated later
            success=True,
        )

        try:
            response = await call_next(request)

            # Record cache hits/misses if applicable
            if "X-Cache" in response.headers:
                if response.headers["X-Cache"] == "HIT":
                    self.analytics_service.record_cache_hit()
                else:
                    self.analytics_service.record_cache_miss()

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            self.analytics_service.record_request(
                endpoint=request.url.path,
                response_time=time.time() - start_time,
                success=False,
            )
            raise

        # Calculate and record response time
        response_time = time.time() - start_time
        self.analytics_service.record_request(
            endpoint=request.url.path, response_time=response_time, success=True
        )

        # Add analytics headers to response
        response.headers["X-Request-Time"] = f"{response_time:.2f}s"
        response.headers[
            "X-Cache-Hit-Rate"
        ] = f"{self.analytics_service.get_metrics()['cache_hit_rate']:.2f}%"

        return response
