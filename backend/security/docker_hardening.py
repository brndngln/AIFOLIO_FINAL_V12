"""
AIFOLIO Hardened Docker Images
Static, deterministic, SAFE AI-compliant Dockerfile generator and audit logger.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_DOCKERFILE = '''
FROM python:3.11-slim
LABEL maintainer="OWNER"
RUN useradd -m aifolio && mkdir /app && chown aifolio /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
USER aifolio
CMD ["python", "-m", "backend.main"]
'''

def get_hardened_dockerfile() -> str:
    logger.info("Generated static hardened Dockerfile")
    return STATIC_DOCKERFILE
