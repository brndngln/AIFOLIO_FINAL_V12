"""
AIFOLIO™ Backend API for SAFE Empire Build
- Serves audit logs, policy versions, webhook events, refund suggestions, and all SAFE AI module outputs
- Triggers SAFE AI automation
- Enforces SAFE AI Charter
"""
from fastapi import FastAPI
import os
import json
from autonomy.ai_static import (
    policy_audit_bot,
    gdpr_ccpa_audit_bot,
    policy_version_tracker,
    refund_optimizer,
    prompt_fingerprinting_engine,
    safe_style_voice_tuner,
    vocabulary_scope_limiter,
    auto_variant_generator,
    audit_timestamp_injector,
    anti_static_guard,
)

# Helper for reading log files


def read_log_lines(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


app = FastAPI()
DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../distribution/legal_exports/")
)
LEGAL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../autonomy/legal/")
)


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


# === PHASE 8 SAFE AI MODULE ENDPOINTS ===
@app.get("/api/phase8/global_failover_log")
def get_global_failover_log():
    return read_log_lines("global_failover_log.txt")


@app.get("/api/phase8/multi_cloud_deployment_log")
def get_multi_cloud_deployment_log():
    return read_log_lines("multi_cloud_deployment_log.txt")


@app.get("/api/phase8/load_forecasting_log")
def get_load_forecasting_log():
    return read_log_lines("load_forecasting_log.txt")


@app.get("/api/phase8/geo_latency_log")
def get_geo_latency_log():
    return read_log_lines("geo_latency_log.txt")


@app.get("/api/phase8/distributed_pipeline_log")
def get_distributed_pipeline_log():
    return read_log_lines("distributed_pipeline_log.txt")


@app.get("/api/phase8/multi_agent_load_balancer_log")
def get_multi_agent_load_balancer_log():
    return read_log_lines("multi_agent_load_balancer_log.txt")


@app.get("/api/phase8/ai_self_audit_log")
def get_ai_self_audit_log():
    return read_log_lines("ai_self_audit_log.txt")


@app.get("/api/phase8/black_box_anomaly_log")
def get_black_box_anomaly_log():
    return read_log_lines("black_box_anomaly_log.txt")


@app.get("/api/phase8/ai_test_sandbox_log")
def get_ai_test_sandbox_log():
    return read_log_lines("ai_test_sandbox_log.txt")


@app.get("/api/phase8/bias_trend_log")
def get_bias_trend_log():
    return read_log_lines("bias_trend_log.txt")


@app.get("/api/phase8/drift_detection_log")
def get_drift_detection_log():
    return read_log_lines("drift_detection_log.txt")


@app.get("/api/phase8/market_adjacency_map_log")
def get_market_adjacency_map_log():
    return read_log_lines("market_adjacency_map_log.txt")


@app.get("/api/phase8/vault_meta_market_log")
def get_vault_meta_market_log():
    return read_log_lines("vault_meta_market_log.txt")


@app.get("/api/phase8/competitor_intel_log")
def get_competitor_intel_log():
    return read_log_lines("competitor_intel_log.txt")


@app.get("/api/phase8/ecosystem_health_log")
def get_ecosystem_health_log():
    return read_log_lines("ecosystem_health_log.txt")


@app.get("/api/phase8/threat_radar_log")
def get_threat_radar_log():
    return read_log_lines("threat_radar_log.txt")


@app.get("/api/phase8/price_sensitivity_map_log")
def get_price_sensitivity_map_log():
    return read_log_lines("price_sensitivity_map_log.txt")


@app.get("/api/phase8/buyer_sentiment_log")
def get_buyer_sentiment_log():
    return read_log_lines("buyer_sentiment_log.txt")


@app.get("/api/phase8/revenue_curve_forecast_log")
def get_revenue_curve_forecast_log():
    return read_log_lines("revenue_curve_forecast_log.txt")


@app.get("/api/phase8/cashflow_projection_log")
def get_cashflow_projection_log():
    return read_log_lines("cashflow_projection_log.txt")


@app.get("/api/phase8/vault_pnl_log")
def get_vault_pnl_log():
    return read_log_lines("vault_pnl_log.txt")


@app.get("/api/phase8/refund_risk_scan_log")
def get_refund_risk_scan_log():
    return read_log_lines("refund_risk_scan_log.txt")


@app.get("/api/phase8/regional_profitability_log")
def get_regional_profitability_log():
    return read_log_lines("regional_profitability_log.txt")


@app.get("/api/phase8/compliance_tree_log")
def get_compliance_tree_log():
    return read_log_lines("compliance_tree_log.txt")


@app.get("/api/phase8/global_tax_sync_log")
def get_global_tax_sync_log():
    return read_log_lines("global_tax_sync_log.txt")


@app.get("/api/phase8/regulatory_horizon_log")
def get_regulatory_horizon_log():
    return read_log_lines("regulatory_horizon_log.txt")


@app.get("/api/phase8/ip_violation_log")
def get_ip_violation_log():
    return read_log_lines("ip_violation_log.txt")


@app.get("/api/phase8/data_sovereignty_log")
def get_data_sovereignty_log():
    return read_log_lines("data_sovereignty_log.txt")


@app.get("/api/phase8/public_complaint_risk_log")
def get_public_complaint_risk_log():
    return read_log_lines("public_complaint_risk_log.txt")


@app.get("/api/phase8/buyer_journey_log")
def get_buyer_journey_log():
    return read_log_lines("buyer_journey_log.txt")


@app.get("/api/phase8/loyalty_program_log")
def get_loyalty_program_log():
    return read_log_lines("loyalty_program_log.txt")


@app.get("/api/phase8/referral_engine_log")
def get_referral_engine_log():
    return read_log_lines("referral_engine_log.txt")


@app.get("/api/phase8/content_gap_log")
def get_content_gap_log():
    return read_log_lines("content_gap_log.txt")


@app.get("/api/phase8/future_vault_log")
def get_future_vault_log():
    return read_log_lines("future_vault_log.txt")


@app.get("/api/phase8/cross_market_promo_log")
def get_cross_market_promo_log():
    return read_log_lines("cross_market_promo_log.txt")


@app.get("/api/phase8/seasonal_campaign_log")
def get_seasonal_campaign_log():
    return read_log_lines("seasonal_campaign_log.txt")


@app.get("/api/phase8/revenue_reconciliation_log")
def get_revenue_reconciliation_log():
    return read_log_lines("revenue_reconciliation_log.txt")


@app.get("/api/phase8/vault_lifecycle_log")
def get_vault_lifecycle_log():
    return read_log_lines("vault_lifecycle_log.txt")


@app.get("/api/phase8/cold_vault_detection_log")
def get_cold_vault_detection_log():
    return read_log_lines("cold_vault_detection_log.txt")


@app.get("/api/phase8/archive_optimization_log")
def get_archive_optimization_log():
    return read_log_lines("archive_optimization_log.txt")


@app.get("/api/phase8/supply_demand_imbalance_log")
def get_supply_demand_imbalance_log():
    return read_log_lines("supply_demand_imbalance_log.txt")


@app.get("/api/phase8/legal_event_watch_log")
def get_legal_event_watch_log():
    return read_log_lines("legal_event_watch_log.txt")


@app.get("/api/phase8/ai_safety_signature_log")
def get_ai_safety_signature_log():
    return read_log_lines("ai_safety_signature_log.txt")


@app.get("/api/phase8/customer_satisfaction_log")
def get_customer_satisfaction_log():
    return read_log_lines("customer_satisfaction_log.txt")


@app.get("/api/phase8/external_channel_risk_log")
def get_external_channel_risk_log():
    return read_log_lines("external_channel_risk_log.txt")


@app.get("/api/phase8/customer_segment_log")
def get_customer_segment_log():
    return read_log_lines("customer_segment_log.txt")


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
    safe = anti_static_guard.scan_for_sentience(text)
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
