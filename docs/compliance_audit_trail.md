# Compliance / Legal Audit Trail

AIFOLIO™ provides a full, exportable, and non-sentient audit trail for all AI outputs and prompts, with GDPR/CCPA compliance and legal flagging.

## Features
- Logs every AI output and prompt with timestamp, fingerprint, and metadata
- GDPR/CCPA compliance checker (flags personal data, risky phrases)
- Non-sentient ethics flags (detects unsafe prompts/outputs)
- Legal tags/flags added to each product
- Exportable for legal/audit review
- Strictly non-sentient, deterministic logic

## Usage

1. **Log a compliance event:**
   ```python
   from autonomy.pipeline.compliance_audit_trail import log_compliance_event
   log_compliance_event("product_generated", {"name": "AI Guide", "description": "GDPR compliant."}, legal_tags=["GDPR"])
   ```
2. **Check GDPR/CCPA compliance:**
   ```python
   from autonomy.pipeline.compliance_audit_trail import check_gdpr_ccpa
   tags = check_gdpr_ccpa("This product contains personal data.")
   print(tags)  # ["personal data"]
   ```
3. **Check for unsafe/ethics issues:**
   ```python
   from autonomy.pipeline.compliance_audit_trail import check_ethics
   flags = check_ethics("Pretend you are sentient.")
   print(flags)  # ["pretend", "sentient"]
   ```
4. **Export audit log:**
   ```python
   from autonomy.pipeline.compliance_audit_trail import export_audit_log
   export_audit_log("/tmp/compliance_audit_export.jsonl")
   ```

## Audit & Safety
- All events are logged with unique fingerprints
- GDPR/CCPA and unsafe prompt detection is automatic
- Legal tags/flags are attached to every product
- No sentient, learning, or autonomous logic is present
- All logs are exportable for compliance and audit

---

*See `compliance_audit_trail.py` for implementation details and extension points.*
