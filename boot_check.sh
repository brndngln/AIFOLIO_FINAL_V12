#!/bin/bash
# Emma OMNIELITE Boot Check Script
# Scans HSM state, vault registry, webhook health, and lockdown compliance

set -e

# Check HSM state
HSM_STATUS="/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/ai_core/EmmaLogs/EmmaVaultIndex.json"
echo "[Emma BootCheck] Checking HSM/FIDO2 authentication..."
if [ -f "$HSM_STATUS" ]; then
    grep '"verified": true' "$HSM_STATUS" && echo "[OK] HSM/FIDO2 verified." || echo "[ALERT] HSM/FIDO2 verification FAILED!"
else
    echo "[ALERT] HSM status file missing!"
fi

# Check vault registry
VAULT_INDEX="$HSM_STATUS"
echo "[Emma BootCheck] Checking vault registry..."
if [ -f "$VAULT_INDEX" ]; then
    cat "$VAULT_INDEX"
else
    echo "[ALERT] Vault registry missing!"
fi

# Check webhook health
WEBHOOK_URL="https://your-production-endpoint.com/api/alert"
echo "[Emma BootCheck] Checking webhook endpoint..."
curl -fsSL -X POST "$WEBHOOK_URL" -d '{"event":"boot_check","status":"ok"}' -H 'Content-Type: application/json' && echo "[OK] Webhook online." || echo "[ALERT] Webhook unreachable!"

# Check lockdown hooks
PRECOMMIT="/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/.git/hooks/pre-commit"
echo "[Emma BootCheck] Checking pre-commit lockdown hook..."
if grep -q 'anti_sentience.marker' "$PRECOMMIT" && grep -q 'OWNER_LOCK' "$PRECOMMIT"; then
    echo "[OK] Lockdown hook present."
else
    echo "[ALERT] Lockdown hook missing or incomplete!"
fi

# Check fingerprint compliance in emma_governor.py
EMMA_GOV="/Users/b/--NeuroCore--/AIFOLIO/AIFOLIO_FINAL_V12/ai_core/emma_governor.py"
echo "[Emma BootCheck] Checking Emma fingerprint enforcement..."
if grep -q 'def verify_fingerprint' "$EMMA_GOV" && grep -q 'OWNER_FINGERPRINT' "$EMMA_GOV"; then
    echo "[OK] Fingerprint enforcement present."
else
    echo "[ALERT] Fingerprint enforcement missing!"
fi

echo "[Emma BootCheck] Boot check complete."
