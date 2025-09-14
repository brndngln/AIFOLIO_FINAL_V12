#!/bin/bash

# AIFOLIO Elite Deployment Script
# Phase 1.11 - Advanced CI/CD Integration
# Zero-downtime production deployment

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEPLOYMENT_ENV="${1:-staging}"
VERSION="${2:-latest}"
BACKUP_ENABLED="${BACKUP_ENABLED:-true}"
HEALTH_CHECK_TIMEOUT="${HEALTH_CHECK_TIMEOUT:-300}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Error handling
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Deployment failed with exit code $exit_code"
        log_info "Rolling back to previous version..."
        rollback_deployment
    fi
    exit $exit_code
}

trap cleanup EXIT

# Validate environment
validate_environment() {
    log_info "🔍 Validating deployment environment..."

    # Check required tools
    local required_tools=("docker" "docker-compose" "curl" "jq")
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "Required tool '$tool' is not installed"
            exit 1
        fi
    done

    # Check environment file
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        log_warning ".env file not found, using defaults"
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    fi

    # Validate Docker daemon
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi

    log_success "Environment validation complete"
}

# Pre-deployment checks
pre_deployment_checks() {
    log_info "🔍 Running pre-deployment checks..."

    # Check disk space
    local available_space=$(df / | awk 'NR==2 {print $4}')
    local required_space=1048576 # 1GB in KB

    if [ "$available_space" -lt "$required_space" ]; then
        log_error "Insufficient disk space. Required: 1GB, Available: $(($available_space/1024))MB"
        exit 1
    fi

    # Check memory
    local available_memory=$(free -m | awk 'NR==2{print $7}')
    local required_memory=512

    if [ "$available_memory" -lt "$required_memory" ]; then
        log_warning "Low available memory. Available: ${available_memory}MB, Recommended: ${required_memory}MB"
    fi

    # Validate configuration files
    if [ ! -f "$PROJECT_ROOT/docker-compose.yml" ]; then
        log_error "docker-compose.yml not found"
        exit 1
    fi

    # Test configuration
    docker-compose -f "$PROJECT_ROOT/docker-compose.yml" config > /dev/null

    log_success "Pre-deployment checks complete"
}

# Create backup
create_backup() {
    if [ "$BACKUP_ENABLED" != "true" ]; then
        log_info "Backup disabled, skipping..."
        return 0
    fi

    log_info "📦 Creating backup..."

    local backup_dir="$PROJECT_ROOT/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"

    # Backup database
    if docker-compose ps | grep -q postgres; then
        log_info "Backing up PostgreSQL database..."
        docker-compose exec -T postgres pg_dump -U aifolio aifolio > "$backup_dir/database.sql"
    fi

    # Backup application data
    if [ -d "$PROJECT_ROOT/data" ]; then
        log_info "Backing up application data..."
        tar -czf "$backup_dir/app_data.tar.gz" -C "$PROJECT_ROOT" data/
    fi

    # Backup configuration
    log_info "Backing up configuration files..."
    cp "$PROJECT_ROOT/.env" "$backup_dir/"
    cp "$PROJECT_ROOT/docker-compose.yml" "$backup_dir/"

    echo "$backup_dir" > "$PROJECT_ROOT/.last_backup"
    log_success "Backup created at $backup_dir"
}

# Build and deploy
deploy_application() {
    log_info "🚀 Deploying AIFOLIO Elite v$VERSION to $DEPLOYMENT_ENV..."

    cd "$PROJECT_ROOT"

    # Set environment-specific variables
    export COMPOSE_PROJECT_NAME="aifolio-${DEPLOYMENT_ENV}"
    export IMAGE_TAG="$VERSION"

    # Build images
    log_info "Building Docker images..."
    docker-compose build --parallel --pull

    # Start services with zero-downtime deployment
    if [ "$DEPLOYMENT_ENV" = "production" ]; then
        log_info "Performing zero-downtime deployment..."

        # Scale up new instances
        docker-compose up -d --scale aifolio-app=2 --no-recreate

        # Wait for health checks
        wait_for_health_check

        # Scale down old instances
        docker-compose up -d --scale aifolio-app=1 --remove-orphans
    else
        # Standard deployment for staging
        log_info "Performing standard deployment..."
        docker-compose up -d --remove-orphans
    fi

    # Wait for services to be ready
    wait_for_services()

    log_success "Deployment complete"
}

# Wait for health checks
wait_for_health_check() {
    log_info "⏳ Waiting for health checks..."

    local timeout=$HEALTH_CHECK_TIMEOUT
    local elapsed=0
    local interval=10

    while [ $elapsed -lt $timeout ]; do
        if curl -f -s http://localhost/health > /dev/null; then
            log_success "Health check passed"
            return 0
        fi

        log_info "Health check failed, retrying in ${interval}s... (${elapsed}/${timeout}s)"
        sleep $interval
        elapsed=$((elapsed + interval))
    done

    log_error "Health check timeout after ${timeout}s"
    return 1
}

# Wait for all services
wait_for_services() {
    log_info "⏳ Waiting for all services to be ready..."

    local services=("aifolio-app" "postgres" "redis")

    for service in "${services[@]}"; do
        log_info "Checking $service..."

        local retries=30
        while [ $retries -gt 0 ]; do
            if docker-compose ps "$service" | grep -q "Up (healthy)"; then
                log_success "$service is ready"
                break
            fi

            if [ $retries -eq 1 ]; then
                log_error "$service failed to start"
                return 1
            fi

            retries=$((retries - 1))
            sleep 5
        done
    done

    log_success "All services are ready"
}

# Post-deployment verification
post_deployment_verification() {
    log_info "🔍 Running post-deployment verification..."

    # Test API endpoints
    local endpoints=(
        "http://localhost/health"
        "http://localhost/api/status"
    )

    for endpoint in "${endpoints[@]}"; do
        log_info "Testing $endpoint..."

        if curl -f -s "$endpoint" > /dev/null; then
            log_success "$endpoint is responding"
        else
            log_error "$endpoint is not responding"
            return 1
        fi
    done

    # Check service logs for errors
    log_info "Checking service logs..."

    local error_count=$(docker-compose logs --tail=100 | grep -i error | wc -l)
    if [ "$error_count" -gt 0 ]; then
        log_warning "Found $error_count error(s) in logs"
        docker-compose logs --tail=20 | grep -i error
    else
        log_success "No errors found in logs"
    fi

    # Performance check
    log_info "Running performance check..."
    local response_time=$(curl -o /dev/null -s -w '%{time_total}' http://localhost/health)
    local response_time_ms=$(echo "$response_time * 1000" | bc)

    if (( $(echo "$response_time < 1.0" | bc -l) )); then
        log_success "Response time: ${response_time_ms}ms (Good)"
    else
        log_warning "Response time: ${response_time_ms}ms (Slow)"
    fi

    log_success "Post-deployment verification complete"
}

# Rollback deployment
rollback_deployment() {
    log_warning "🔄 Rolling back deployment..."

    if [ -f "$PROJECT_ROOT/.last_backup" ]; then
        local backup_dir=$(cat "$PROJECT_ROOT/.last_backup")

        if [ -d "$backup_dir" ]; then
            log_info "Restoring from backup: $backup_dir"

            # Stop current services
            docker-compose down

            # Restore configuration
            cp "$backup_dir/.env" "$PROJECT_ROOT/"
            cp "$backup_dir/docker-compose.yml" "$PROJECT_ROOT/"

            # Restore database
            if [ -f "$backup_dir/database.sql" ]; then
                docker-compose up -d postgres
                sleep 10
                docker-compose exec -T postgres psql -U aifolio -d aifolio < "$backup_dir/database.sql"
            fi

            # Restore application data
            if [ -f "$backup_dir/app_data.tar.gz" ]; then
                tar -xzf "$backup_dir/app_data.tar.gz" -C "$PROJECT_ROOT"
            fi

            # Restart services
            docker-compose up -d

            log_success "Rollback complete"
        else
            log_error "Backup directory not found: $backup_dir"
        fi
    else
        log_error "No backup information found"
    fi
}

# Cleanup old resources
cleanup_old_resources() {
    log_info "🧹 Cleaning up old resources..."

    # Remove unused Docker images
    docker image prune -f

    # Remove old backups (keep last 7 days)
    find "$PROJECT_ROOT/backups" -type d -mtime +7 -exec rm -rf {} + 2>/dev/null || true

    # Remove old logs
    find "$PROJECT_ROOT/logs" -name "*.log" -mtime +30 -delete 2>/dev/null || true

    log_success "Cleanup complete"
}

# Send deployment notification
send_notification() {
    local status="$1"
    local message="$2"

    log_info "📢 Sending deployment notification..."

    # Webhook notification (if configured)
    if [ -n "${WEBHOOK_URL:-}" ]; then
        curl -X POST "$WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "{
                \"text\": \"AIFOLIO Elite Deployment\",
                \"attachments\": [{
                    \"color\": \"$([ "$status" = "success" ] && echo "good" || echo "danger")\",
                    \"fields\": [{
                        \"title\": \"Environment\",
                        \"value\": \"$DEPLOYMENT_ENV\",
                        \"short\": true
                    }, {
                        \"title\": \"Version\",
                        \"value\": \"$VERSION\",
                        \"short\": true
                    }, {
                        \"title\": \"Status\",
                        \"value\": \"$status\",
                        \"short\": true
                    }, {
                        \"title\": \"Message\",
                        \"value\": \"$message\",
                        \"short\": false
                    }]
                }]
            }" > /dev/null 2>&1 || log_warning "Failed to send webhook notification"
    fi

    log_success "Notification sent"
}

# Main deployment function
main() {
    log_info "🚀 Starting AIFOLIO Elite deployment..."
    log_info "Environment: $DEPLOYMENT_ENV"
    log_info "Version: $VERSION"
    log_info "Backup: $BACKUP_ENABLED"

    validate_environment
    pre_deployment_checks
    create_backup
    deploy_application
    post_deployment_verification
    cleanup_old_resources

    local deployment_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    send_notification "success" "Deployment completed successfully at $deployment_time"

    log_success "🎉 AIFOLIO Elite v$VERSION deployed successfully to $DEPLOYMENT_ENV!"
    log_info "🔗 Application URL: http://localhost"
    log_info "📊 Monitoring: http://localhost:PORT (if enabled)"
    log_info "📋 Logs: docker-compose logs -f"
}

# Script usage
usage() {
    echo "Usage: $0 [environment] [version]"
    echo ""
    echo "Arguments:"
    echo "  environment    Deployment environment (staging|production) [default: staging]"
    echo "  version        Application version to deploy [default: latest]"
    echo ""
    echo "Environment Variables:"
    echo "  BACKUP_ENABLED         Enable/disable backup creation [default: true]"
    echo "  HEALTH_CHECK_TIMEOUT   Health check timeout in seconds [default: 300]"
    echo "  WEBHOOK_URL           Webhook URL for notifications [optional]"
    echo ""
    echo "Examples:"
    echo "  $0 staging"
    echo "  $0 production v1.11.0"
    echo "  BACKUP_ENABLED=false $0 staging"
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        usage
        exit 0
        ;;
    staging|production)
        main "$@"
        ;;
    "")
        main staging
        ;;
    *)
        log_error "Invalid environment: $1"
        usage
        exit 1
        ;;
esac
