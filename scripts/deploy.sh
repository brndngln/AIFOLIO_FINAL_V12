#!/bin/bash
# AIFOLIO Deployment Script

set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "🚀 Deploying AIFOLIO to $ENVIRONMENT (version: $VERSION)"

# Validate environment
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "❌ Invalid environment. Use 'staging' or 'production'"
    exit 1
fi

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."
python scripts/validate_env.py
if [ $? -ne 0 ]; then
    echo "❌ Environment validation failed"
    exit 1
fi

# Run tests
echo "🧪 Running test suite..."
python -m pytest tests/ --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests failed"
    exit 1
fi

# Build and deploy
echo "🏗️  Building application..."
python setup.py build

echo "📦 Creating deployment package..."
tar -czf aifolio-$VERSION.tar.gz dist/

echo "🚀 Deploying to $ENVIRONMENT..."
# Add actual deployment commands here

echo "✅ Deployment completed successfully!"
