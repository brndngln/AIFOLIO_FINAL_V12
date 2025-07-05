#!/bin/bash
set -e

echo "🔐 Building and Running Emma Docker Containers..."

docker build -t emma_hsm_auth -f emma_hsm_auth.Dockerfile .
docker run -d --name emma_hsm_auth_container emma_hsm_auth

docker build -t emma_quantum_logger -f emma_quantum_logger.Dockerfile .
docker run -d --name emma_quantum_logger_container emma_quantum_logger

docker build -t emma_fingerprint_monitor -f emma_fingerprint_monitor.Dockerfile .
docker run -d --name emma_fingerprint_monitor_container emma_fingerprint_monitor

echo "✅ All containers are up and running."
