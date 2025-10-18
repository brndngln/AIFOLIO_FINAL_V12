#!/bin/bash
set -e
mkdir -p /opt/emma_logs/
exec python emma_remote_logger.py
