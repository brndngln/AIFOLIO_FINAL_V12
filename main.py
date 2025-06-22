from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from backend.ai_prompt_engine.generate_vault import generate_vault_prompt
from backend.pdf_builder.render_pdf import build_pdf
from backend.ai_cover_creator.dalle import generate_cover
from backend.product_prep.zip_packager import package_vault
from backend.marketing.generate_copy import generate_marketing_copy
from backend.dashboard.notion_push import push_to_notion
from backend.utils.api_utils import api_error_handler
from backend.utils.ai_safety import AISafety
from backend.analytics.analytics_middleware import AnalyticsMiddleware
from backend.analytics.analytics_service import AnalyticsService
from backend.ab_testing.ab_testing_service import ABTestingService
from backend.utils.error_handler import ErrorHandler
from backend.cache.cache_service import CacheService
from backend.rate_limiting.rate_limiter import RateLimiter
import logging
from typing import Dict
from redis import Redis
import os

# Initialize Redis client
redis_client = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0
)

# Initialize services
analytics_service = AnalyticsService(redis_client)
ab_testing_service = ABTestingService(redis_client)
error_handler = ErrorHandler(
    redis_client,
    sentry_dsn=os.getenv('SENTRY_DSN')
)
cache_service = CacheService(redis_client, default_ttl=3600)
rate_limiter = RateLimiter(redis_client, default_limit=60, default_window=60)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize AI safety system
ai_safety = AISafety()

# Initialize app
app = FastAPI(
    title="AIFOLIO API",
    description="AI-powered Digital Product Creation Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add analytics middleware
app.add_middleware(AnalyticsMiddleware, redis_client=redis_client)

# Add AI safety middleware
@app.middleware("http")
async def ai_safety_middleware(request: Request, call_next):
    try:
        # Check rate limits
        if not ai_safety.check_rate_limit(request):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded"
            )

        # Validate content
        if request.method in ["POST", "PUT"]:
            content = await request.body()
            if not ai_safety.validate_content(content.decode()):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Content validation failed"
                )

        response = await call_next(request)
        return response

    except Exception as e:
        error = api_error_handler.handle_error(e)
        logger.error(f"AI safety middleware failed: {error.message}")
        raise error

# Add monitoring endpoint
@app.get("/monitor")
async def get_system_metrics():
    """Get system metrics and status."""
    metrics = ai_safety.monitor_system()
    return {
        "status": "healthy",
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }

# Add analytics endpoint
@app.get("/analytics")
async def get_analytics():
    """Get analytics data for the dashboard."""
    return analytics_service.get_metrics()

# Cache management endpoints
@app.get("/cache/metrics")
async def get_cache_metrics():
    """Get cache metrics."""
    return cache_service.get_metrics()

# Rate limiting endpoints
@app.get("/rate-limit/status/{key}")
async def get_rate_limit_status(key: str):
    """Get rate limit status for a key."""
    return rate_limiter.get_rate_limit_status(key)

@app.post("/rate-limit/clear/{key}")
async def clear_rate_limit(key: str):
    """Clear rate limit for a key."""
    rate_limiter.clear_rate_limit(key)
    return {"status": "cleared"}

@app.get("/rate-limit/metrics")
async def get_rate_limit_metrics():
    """Get rate limiting metrics."""
    return rate_limiter.get_metrics()

@app.post("/cache/clear")
async def clear_cache(pattern: str = '*'):
    """Clear cache entries matching pattern."""
    cleared = cache_service.clear_cache(pattern)
    return {"cleared": cleared}

# Error handling endpoints
@app.get("/errors/{error_id}")
async def get_error(error_id: str):
    """Get details of a specific error."""
    error = error_handler.get_error(error_id)
    if error:
        return error
    raise HTTPException(status_code=404, detail="Error not found")

@app.get("/errors/recent")
async def get_recent_errors(limit: int = 10):
    """Get recent errors."""
    return error_handler.get_recent_errors(limit)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    error_response = error_handler.handle_error(exc, {
        "endpoint": request.url.path,
        "method": request.method,
        "headers": dict(request.headers)
    })
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response
    )

# A/B Testing endpoints
@app.post("/ab-tests")
async def create_ab_test(name: str, variants: Dict[str, float], duration_days: int = 7):
    """Create a new A/B test."""
    test_id = ab_testing_service.create_test(name, variants, duration_days)
    return {"test_id": test_id}

@app.get("/ab-tests/{test_id}")
async def get_ab_test(test_id: str):
    """Get A/B test details and metrics."""
    test = ab_testing_service.get_test(test_id)
    if test:
        return {
            "test": {
                "name": test.name,
                "variants": test.variants,
                "start_date": test.start_date.isoformat(),
                "end_date": test.end_date.isoformat()
            },
            "metrics": test.get_metrics()
        }
    raise HTTPException(status_code=404, detail="Test not found")

@app.get("/ab-tests/{test_id}/variant")
async def get_ab_test_variant(test_id: str, user_id: str):
    """Get the variant for a specific user."""
    test = ab_testing_service.get_test(test_id)
    if test:
        return {"variant": test.get_variant(user_id)}
    raise HTTPException(status_code=404, detail="Test not found")

@app.post("/ab-tests/{test_id}/result")
async def record_ab_test_result(test_id: str, user_id: str, variant: str, converted: bool = False):
    """Record an A/B test result."""
    ab_testing_service.record_test_result(test_id, user_id, variant, converted)
    return {"status": "success"}

# 📥 Request model for POST vault generation
class VaultRequest(BaseModel):
    topic: str
    user_id: Optional[str] = None
    ip_address: Optional[str] = None

# Custom exception handler
@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    error_response = api_error_handler.handle_error(exc)
    return JSONResponse(
        status_code=error_response.status_code,
        content=error_response.to_dict()
    )

# 🚀 POST endpoint for custom vault generation via OpenAI
@app.post("/generate-vault")
async def generate_custom_vault(request: Request, vault_request: VaultRequest):
    try:
        # Rate limit check
        if not rate_limiter.check_limit(request):
            raise api_error_handler.create_error(
                "RateLimitError",
                "Rate limit exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        logger.info(f"Generating vault for topic: {vault_request.topic}")
        
        # Update the prompt to include the topic
        content = generate_vault_prompt(vault_request.topic)
        
        return {
            "status": "success",
            "message": "Vault generated successfully",
            "vault": content
        }
    except Exception as e:
        error = api_error_handler.handle_error(e)
        logger.error(f"Error generating vault: {error.message}")
        raise error

# 🧠 GET endpoint for full auto pipeline
@app.get("/generate-vault")
async def generate_full_vault(request: Request):
    try:
        # Rate limit check
        if not rate_limiter.check_limit(request):
            raise api_error_handler.create_error(
                "RateLimitError",
                "Rate limit exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        logger.info("Starting vault generation process")
        
        # 1. Generate vault content
        logger.info("Generating vault content...")
        vault_data = generate_vault_prompt()
        
        # 2. Generate cover
        logger.info("Generating cover image...")
        generate_cover(vault_data['title'], vault_data['description'])
        
        # 3. Build PDF
        logger.info("Building PDF...")
        build_pdf(vault_data)
        
        # 4. Package for export
        logger.info("Packaging vault...")
        package_vault(vault_data['title'])
        
        # 5. Create marketing copy
        logger.info("Generating marketing copy...")
        generate_marketing_copy(vault_data)
        
        # 6. Push vault data to Notion dashboard
        logger.info("Updating Notion dashboard...")
        push_to_notion(vault_data)
        
        logger.info(f"Vault '{vault_data['title']}' generated successfully")
        return {
            "status": "success",
            "message": "Vault generated successfully",
            "vault": {
                "title": vault_data['title'],
                "description": vault_data['description'],
                "chapters": vault_data['chapters'],
                "cta": vault_data['cta']
            }
        }
    except Exception as e:
        error = api_error_handler.handle_error(e)
        logger.error(f"Vault generation failed: {error.message}")
        raise error

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}