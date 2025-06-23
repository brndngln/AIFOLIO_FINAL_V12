"""
AIFOLIO SAFE AI Pipeline Monitoring Module
- Tracks API failures, email delivery %, vault build failures, legal compliance passes/fails
- Logs to /pipeline/health_log.json
- No optimization, no static, no static logic
"""
import os
import json
from datetime import datetime

HEALTH_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), 'health_log.json'))

def log_pipeline_health(api_failures, email_deliveries, vault_builds, compliance_checks):
    log = {
        'timestamp': datetime.utcnow().isoformat(),
        'api_failures': api_failures,
        'email_delivery_percent': email_deliveries,
        'vault_build_failures': vault_builds,
        'compliance_passes': compliance_checks
    }
    with open(HEALTH_LOG, 'a') as f:
        f.write(json.dumps(log) + '\n')
    return log
