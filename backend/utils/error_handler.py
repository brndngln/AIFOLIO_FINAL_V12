import logging
from typing import Dict, Any, Optional
from datetime import datetime
import json
import uuid
from redis import Redis
import sentry_sdk
from sentry_sdk.integrations.redis import RedisIntegration

logger = logging.getLogger(__name__)

class ErrorHandler:
    def __init__(self, redis_client: Redis, sentry_dsn: Optional[str] = None):
        self.redis = redis_client
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[RedisIntegration()],
                traces_sample_rate=1.0
            )

    def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle and log an error."""
        error_id = self._generate_error_id()
        error_data = self._format_error_data(error, context)
        
        # Log error
        logger.error(f"Error {error_id}: {str(error)}", extra=error_data)
        
        # Store in Redis
        self._store_error(error_id, error_data)
        
        # Send to Sentry if configured
        if sentry_sdk.Hub.current.client:
            sentry_sdk.capture_exception(error)
        
        return {
            "error_id": error_id,
            "message": str(error),
            "timestamp": error_data['timestamp']
        }

    def _generate_error_id(self) -> str:
        """Generate a unique error ID."""
        return f"ERR_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4()}"

    def _format_error_data(self, error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format error data for logging and storage."""
        return {
            "type": error.__class__.__name__,
            "message": str(error),
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "stack_trace": self._get_stack_trace(error)
        }

    def _get_stack_trace(self, error: Exception) -> str:
        """Get formatted stack trace."""
        import traceback
        return ''.join(traceback.format_exception(type(error), error, error.__traceback__))

    def _store_error(self, error_id: str, error_data: Dict[str, Any]):
        """Store error data in Redis."""
        key = f"error:{error_id}"
        self.redis.set(key, json.dumps(error_data))
        self.redis.expire(key, 86400)  # 24 hours TTL

    def get_error(self, error_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored error data by ID."""
        key = f"error:{error_id}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def get_recent_errors(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent errors."""
        errors = {}
        for key in self.redis.scan_iter("error:*"):
            error_id = key.decode().split(':')[1]
            error_data = json.loads(self.redis.get(key))
            errors[error_id] = error_data
            if len(errors) >= limit:
                break
        return errors
