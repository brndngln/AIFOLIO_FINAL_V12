# AIFOLIO Elite Production Dockerfile
# Phase 1.11 - Advanced CI/CD Integration
# Multi-stage build for optimized production deployment

# Stage 1: Build Environment
FROM node:18.17.0-alpine AS builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    make \
    g++ \
    git \
    curl

# Copy package files
COPY config/package*.json ./

# Install Node.js dependencies
RUN npm ci --only=production --prefer-offline --no-audit

# Copy source code
COPY . .

# Create build info
RUN echo '{"version":"1.11.0","buildDate":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","commit":"'${GITHUB_SHA:-unknown}'"}' > build-info.json

# Stage 2: Python Environment
FROM python:3.11-alpine AS python-builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install \
    flask==2.3.3 \
    gunicorn==21.2.0 \
    redis==5.0.1 \
    celery==5.3.4 \
    psycopg2-binary==2.9.9 \
    sqlalchemy==2.0.23 \
    alembic==1.13.1

# Stage 3: Production Runtime
FROM node:18.17.0-alpine AS production

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000
ENV PYTHONPATH=/app
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    nginx \
    supervisor \
    curl \
    ca-certificates \
    tzdata

# Create app user
RUN addgroup -g 1001 -S aifolio && \
    adduser -S aifolio -u 1001 -G aifolio

# Set working directory
WORKDIR /app

# Copy Python virtual environment
COPY --from=python-builder /opt/venv /opt/venv

# Copy Node.js dependencies and built application
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/build-info.json ./

# Copy application source
COPY --chown=aifolio:aifolio . .

# Create necessary directories
RUN mkdir -p /var/log/aifolio /var/run/aifolio /app/logs && \
    chown -R aifolio:aifolio /var/log/aifolio /var/run/aifolio /app/logs

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create health check script
RUN cat > /app/healthcheck.sh << 'EOF'
#!/bin/sh
set -e

# Check Node.js service
if ! curl -f http://localhost:3000/health >/dev/null 2>&1; then
    echo "Node.js service health check failed"
    exit 1
fi

# Check Python service (if running)
if pgrep -f "python.*app.py" >/dev/null; then
    if ! curl -f http://localhost:5000/health >/dev/null 2>&1; then
        echo "Python service health check failed"
        exit 1
    fi
fi

echo "All services healthy"
exit 0
EOF

RUN chmod +x /app/healthcheck.sh

# Create startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/sh
set -e

echo "🚀 Starting AIFOLIO Elite Production Server..."

# Ensure log directories exist
mkdir -p /var/log/aifolio /app/logs

# Start supervisord to manage all services
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
EOF

RUN chmod +x /app/start.sh

# Switch to app user
USER aifolio

# Expose ports
EXPOSE 3000 5000 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /app/healthcheck.sh

# Start the application
CMD ["/app/start.sh"]

# Labels for metadata
LABEL maintainer="AIFOLIO Elite Team"
LABEL version="1.11.0"
LABEL description="AIFOLIO Elite - Advanced AI Portfolio Management System"
LABEL org.opencontainers.image.title="AIFOLIO Elite"
LABEL org.opencontainers.image.description="Advanced AI Portfolio Management System with CI/CD Pipeline"
LABEL org.opencontainers.image.version="1.11.0"
LABEL org.opencontainers.image.vendor="AIFOLIO"
LABEL org.opencontainers.image.licenses="MIT"
