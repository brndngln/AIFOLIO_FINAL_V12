"""
AIFOLIO™ Backend API for SAFE Empire Build
- Serves audit logs, policy versions, webhook events, refund suggestions, and all SAFE AI module outputs
- Triggers SAFE AI automation
- Enforces SAFE AI Charter
"""
from fastapi import FastAPI, HTTPException
import os
import json
from autonomy.ai_static import (
    policy_audit_bot, gdpr_ccpa_audit_bot, policy_version_tracker,
    refund_optimizer, prompt_fingerprinting_engine, safe_style_voice_tuner,
    vocabulary_scope_limiter, auto_variant_generator, audit_timestamp_injector,
    anti_sentience_guard
)

# Helper for reading log files
from fastapi.responses import JSONResponse

def read_log_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f.readlines()]

app = FastAPI()
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/'))
LEGAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../autonomy/legal/'))

@app.get("/api/policy_audit_log")
def get_policy_audit_log():
    return read_log_lines("policy_audit_log.txt")

@app.get("/api/gdpr_ccpa_audit_log")
def get_gdpr_ccpa_audit_log():
    return read_log_lines("gdpr_ccpa_audit_log.txt")

@app.get("/api/policy_versions")
def get_policy_versions():
    path = os.path.join(DATA_DIR, "policy_version_log.json")
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)

@app.get("/api/webhook_events")
def get_webhook_events():
    return read_log_lines("webhook_trigger_log.txt")

@app.get("/api/prompt_fingerprint_log")
def get_prompt_fingerprint_log():
    return read_log_lines("prompt_fingerprint_log.txt")

@app.get("/api/style_tuner_log")
def get_style_tuner_log():
    return read_log_lines("style_tuner_log.txt")

@app.get("/api/vocab_limiter_log")
def get_vocab_limiter_log():
    return read_log_lines("vocab_limiter_log.txt")

@app.get("/api/variant_generator_log")
def get_variant_generator_log():
    return read_log_lines("variant_generator_log.txt")

@app.get("/api/audit_timestamp_log")
def get_audit_timestamp_log():
    return read_log_lines("audit_timestamp_log.txt")

@app.get("/api/anti_sentience_log")
def get_anti_sentience_log():
    return read_log_lines("anti_sentience_log.txt")

@app.get("/api/synthetic_monitor_log")
def get_synthetic_monitor_log():
    return read_log_lines("synthetic_monitor_log.txt")

@app.get("/api/webhook_latency_log")
def get_webhook_latency_log():
    return read_log_lines("webhook_latency_log.txt")

@app.get("/api/csv_import_export_log")
def get_csv_import_export_log():
    return read_log_lines("csv_import_export_log.txt")

@app.get("/api/load_balancer_log")
def get_load_balancer_log():
    return read_log_lines("load_balancer_log.txt")

@app.get("/api/cold_start_log")
def get_cold_start_log():
    return read_log_lines("cold_start_log.txt")

@app.get("/api/auto_recovery_log")
def get_auto_recovery_log():
    return read_log_lines("auto_recovery_log.txt")

@app.get("/api/telegram_alert_log")
def get_telegram_alert_log():
    return read_log_lines("telegram_alert_log.txt")

@app.get("/api/refund_suggestions")
def get_refund_suggestions():
    path = os.path.join(DATA_DIR, "refund_log.json")
    if not os.path.exists(path):
        return []
    return refund_optimizer.suggest_refund_action(path)

@app.post("/api/fingerprint_prompt")
def fingerprint_prompt(prompt: str):
    fp = prompt_fingerprinting_engine.fingerprint_prompt(prompt)
    return {"fingerprint": fp}

@app.post("/api/tune_style")
def tune_style(text: str, style: str = "default"):
    tuned = safe_style_voice_tuner.tune_style(text, style)
    return {"tuned": tuned}

@app.post("/api/limit_vocabulary")
def limit_vocabulary(text: str):
    limited = vocabulary_scope_limiter.limit_vocabulary(text)
    return {"limited": limited}

@app.post("/api/generate_variants")
def generate_variants(text: str, templates: list):
    variants = auto_variant_generator.generate_variants(text, templates)
    return {"variants": variants}

@app.post("/api/inject_timestamp")
def inject_timestamp(output: str):
    stamped = audit_timestamp_injector.inject_timestamp(output)
    return {"timestamped": stamped}

@app.post("/api/scan_for_sentience")
def scan_for_sentience(text: str):
    safe = anti_sentience_guard.scan_for_sentience(text)
    return {"safe": safe}

@app.post("/api/audit_policies")
def audit_policies():
    results = policy_audit_bot.audit_all_policies(LEGAL_DIR)
    gdpr_results = gdpr_ccpa_audit_bot.audit_gdpr_ccpa(LEGAL_DIR)
    return {"policy_audit": results, "gdpr_ccpa_audit": gdpr_results}

@app.post("/api/record_policy_version")
def record_version(policy_name: str):
    ok = policy_version_tracker.record_policy_version(LEGAL_DIR, policy_name)
    return {"success": ok}
