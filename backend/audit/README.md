# AIFOLIO SAFE AI Audit & Compliance Modules

This directory contains static, deterministic, SAFE AI-compliant modules for auditing, compliance, and notification integrations. All modules are OWNER-controlled, fully auditable, and contain clear extension points for future real integrations.

## Modules Overview

- **export_audit_trail.py**: Export audit logs as JSON or CSV.
- **webhook_notifications.py**: Static notification hooks for Slack, Discord, Email (env-configured).
- **partner_api_stubs.py**: Static stubs for future partner APIs (legal health, compliance, analytics).
- **full_safe_ai_compliance_audit.py**: Static SAFE AI compliance checklist and audit runner.
- **security_privacy_audit.py**: Static scan for secrets and privacy violations.
- **test_coverage_audit.py**: Static report of test coverage for backend/frontend modules.

## Usage

- All modules are static and deterministic. No adaptive or sentient logic is present.
- All secrets/configs must be set via environment variables.
- For real integrations, follow the documented extension points in each module.

---

**SAFE AI Charter Compliant.**
