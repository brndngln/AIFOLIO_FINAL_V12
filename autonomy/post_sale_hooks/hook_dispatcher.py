import logging
from .send_confirmation_email import send_confirmation_email
from .trigger_upsell_suggestion import trigger_upsell_suggestion
from .log_receipt import log_receipt_to_db
from .update_smart_price import update_smart_price
from .request_review import request_review
from .track_analytics import track_analytics
from .cross_sell_recommender import cross_sell_recommender
from .send_preview_bundle import send_preview_bundle
from .file_tax_compliance import file_tax_compliance
from .tag_buyer_crm import tag_buyer_crm
from .affiliate_attribution import affiliate_attribution
from .fraud_check import fraud_check

from .outbound_webhook import post_sale_event_to_webhooks

from .hook_metrics import hook_metrics

def run_all_hooks(sale_data):
    """
    Run all post-sale hooks. Each hook is retry-safe, logs independently, and cannot block others or delay vault delivery.
    After all hooks, triggers outbound webhooks with the full sale_data and hook results.
    Records metrics for dashboard analytics.
    Returns a summary dict of hook execution results.
    """
    results = {}
    # Send Confirmation Email
    import time
    start = time.time()
    try:
        results['send_confirmation_email'] = send_confirmation_email(sale_data["buyer_email"], sale_data["vault_name"])
        hook_metrics.record('send_confirmation_email', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('send_confirmation_email', False, time.time()-start, error=str(e))
    # Trigger Upsell Suggestion
    start = time.time()
    try:
        results['trigger_upsell_suggestion'] = trigger_upsell_suggestion(sale_data["buyer_email"], sale_data["vault_name"])
        hook_metrics.record('trigger_upsell_suggestion', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('trigger_upsell_suggestion', False, time.time()-start, error=str(e))
    # Log Receipt
    start = time.time()
    try:
        results['log_receipt_to_db'] = log_receipt_to_db({
            "vault": sale_data["vault_id"],
            "buyer": sale_data["buyer_email"],
            "price": sale_data["sale_amount"],
            "timestamp": sale_data["timestamp"]
        })
        hook_metrics.record('log_receipt_to_db', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('log_receipt_to_db', False, time.time()-start, error=str(e))
    # Update Smart Price
    start = time.time()
    try:
        results['update_smart_price'] = update_smart_price(sale_data["vault_id"])
        hook_metrics.record('update_smart_price', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('update_smart_price', False, time.time()-start, error=str(e))
    # Request Review
    start = time.time()
    try:
        results['request_review'] = request_review.schedule_email(sale_data["buyer_email"], delay_hours=24)
        hook_metrics.record('request_review', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('request_review', False, time.time()-start, error=str(e))
    # Track Analytics (anomaly detection)
    start = time.time()
    try:
        analytics_result = track_analytics.record_sale(sale_data["vault_id"], sale_data.get("buyer_metadata", {}))
        anomaly = analytics_result.get('anomaly', False) if isinstance(analytics_result, dict) else False
        results['track_analytics'] = analytics_result
        hook_metrics.record('track_analytics', True, time.time()-start, anomaly=anomaly)
    except Exception as e:
        hook_metrics.record('track_analytics', False, time.time()-start, error=str(e))
    # Cross-sell Recommender
    start = time.time()
    try:
        cross_result = cross_sell_recommender.recommend_next(sale_data["buyer_email"], current_vault=sale_data["vault_id"])
        results['cross_sell_recommender'] = cross_result
        hook_metrics.record('cross_sell_recommender', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('cross_sell_recommender', False, time.time()-start, error=str(e))
    # Send Preview Bundle
    start = time.time()
    try:
        results['send_preview_bundle'] = send_preview_bundle(sale_data["buyer_email"], sale_data.get("vault_preview_data", {}))
        hook_metrics.record('send_preview_bundle', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('send_preview_bundle', False, time.time()-start, error=str(e))
    # File Tax Compliance (compliance)
    start = time.time()
    try:
        compliance_result = file_tax_compliance.trigger(sale_data)
        compliance = compliance_result.get('compliance', False) if isinstance(compliance_result, dict) else False
        results['file_tax_compliance'] = compliance_result
        hook_metrics.record('file_tax_compliance', True, time.time()-start, compliance=compliance)
    except Exception as e:
        hook_metrics.record('file_tax_compliance', False, time.time()-start, error=str(e))
    # Tag Buyer CRM
    start = time.time()
    try:
        results['tag_buyer_crm'] = tag_buyer_crm(sale_data["buyer_email"])
        hook_metrics.record('tag_buyer_crm', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('tag_buyer_crm', False, time.time()-start, error=str(e))
    # Affiliate Attribution
    start = time.time()
    try:
        results['affiliate_attribution'] = affiliate_attribution(sale_data["buyer_email"], sale_data.get("referral_data", {}))
        hook_metrics.record('affiliate_attribution', True, time.time()-start)
    except Exception as e:
        hook_metrics.record('affiliate_attribution', False, time.time()-start, error=str(e))
    # Fraud Check (fraud)
    start = time.time()
    try:
        fraud_result = fraud_check(sale_data.get("buyer_data", {}), sale_data.get("sale_metadata", {}))
        fraud = fraud_result.get('fraud_flag', False) if isinstance(fraud_result, dict) else False
        results['fraud_check'] = fraud_result
        hook_metrics.record('fraud_check', True, time.time()-start, fraud=fraud)
    except Exception as e:
        hook_metrics.record('fraud_check', False, time.time()-start, error=str(e))
    # Outbound webhooks for external integrations
    post_sale_event_to_webhooks("post_sale_hooks_complete", {"sale_data": sale_data, "hook_results": results})
    return results
    try:
        send_preview_bundle(sale_data["buyer_email"], sale_data.get("vault_preview_data", {}))
    except Exception:
        logging.exception("send_preview_bundle failed")
        errors.append("send_preview_bundle")
    try:
        file_tax_compliance.trigger(sale_data)
    except Exception:
        logging.exception("file_tax_compliance failed")
        errors.append("file_tax_compliance")
    try:
        tag_buyer_crm("AI_PDF_BUYER", sale_data["buyer_email"])
    except Exception:
        logging.exception("tag_buyer_crm failed")
        errors.append("tag_buyer_crm")
    try:
        affiliate_attribution(sale_data["buyer_email"], sale_data.get("referral_data", {}))
    except Exception:
        logging.exception("affiliate_attribution failed")
        errors.append("affiliate_attribution")
    try:
        fraud_check(sale_data.get("buyer_data", {}), sale_data.get("sale_metadata", {}))
    except Exception:
        logging.exception("fraud_check failed")
        errors.append("fraud_check")
    if errors:
        logging.error(f"Post-sale hooks completed with errors: {errors}")
    else:
        logging.info("All post-sale hooks completed successfully.")
