"""
FastAPI REST API for AffiliateBooster simulation and reporting
- Each simulation result is automatically exported to Google Sheets and Airtable
- A Zapier webhook is triggered after each simulation or batch

To use real integrations, set your API keys/environment variables in your `.env` file or environment (see integrations/third_party_integrations.py)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from aifolio_empire.sales_marketing_engines.affiliate_booster import AffiliateBooster
from integrations.third_party_integrations import (
    export_to_google_sheets, export_to_airtable, trigger_zapier_webhook
)
import os

app = FastAPI(title="AffiliateBooster API", description="Elite Affiliate Simulation & Reporting API", version="1.0")
booster = AffiliateBooster()

# Example IDs for export (replace with your real IDs or set as env vars)
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "your_google_sheet_id")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "your_airtable_base_id")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "AffiliateReports")

class AffiliateSimRequest(BaseModel):
    product_id: str
    product_name: str
    product_price: float
    affiliate_id: str
    affiliate_name: str
    address_or_ip: str = None  # For real-time jurisdiction lookup

class BatchSimRequest(BaseModel):
    requests: List[AffiliateSimRequest]

@app.post("/simulate-affiliate")
def simulate_affiliate(req: AffiliateSimRequest):
    elements = booster.setup_affiliate_program_elements(
        product_id=req.product_id,
        product_name=req.product_name,
        product_price=req.product_price,
        affiliate_id=req.affiliate_id,
        affiliate_name=req.affiliate_name
    )
    if not elements:
        raise HTTPException(status_code=400, detail="Simulation failed.")
    dashboard = elements.get("simulated_dashboard_snapshot", {})
    report = booster.generate_affiliate_report(req.product_id, req.affiliate_id, dashboard, elements)
    # --- Elite tax reporting ---
    country_code = next(iter(dashboard.get("geo_distribution", {}).keys()), "GLOBAL") if dashboard.get("geo_distribution") else "GLOBAL"
    earnings = elements.get("simulated_earnings_from_snapshot", 0.0)
    tax_report = booster.generate_tax_report(
        product_id=req.product_id,
        affiliate_id=req.affiliate_id,
        country_code=country_code,
        earnings=earnings,
        format="audit"
    )
    # --- Export to Google Sheets ---
    try:
        export_to_google_sheets(GOOGLE_SHEET_ID, [
            elements.get('product_id'),
            elements.get('affiliate_id'),
            elements.get('simulated_earnings_from_snapshot'),
            elements.get('simulated_referral_percentage'),
            elements.get('setup_timestamp_simulated'),
            dashboard.get('fraud_flag'),
            tax_report.get('tax_due'),
            tax_report.get('tax_rate'),
            tax_report.get('tax_fraud_flag')
        ])
    except Exception as e:
        print(f"[Google Sheets] Export failed: {e}")
    # --- Export to Airtable ---
    try:
        export_to_airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, {**elements, **{'tax_due': tax_report.get('tax_due'), 'tax_rate': tax_report.get('tax_rate')}})
    except Exception as e:
        print(f"[Airtable] Export failed: {e}")
    # --- Trigger Zapier webhook ---
    try:
        trigger_zapier_webhook({
            "event": "single_simulation_complete",
            "product_id": req.product_id,
            "affiliate_id": req.affiliate_id,
            "tax_due": tax_report.get('tax_due'),
            "tax_fraud_flag": tax_report.get('tax_fraud_flag')
        })
    except Exception as e:
        print(f"[Zapier] Trigger failed: {e}")
    return {"elements": elements, "report": report, "tax_report": tax_report}

@app.post("/batch-simulate")
def batch_simulate(batch: BatchSimRequest):
    results = []
    for req in batch.requests:
        elements = booster.setup_affiliate_program_elements(
            product_id=req.product_id,
            product_name=req.product_name,
            product_price=req.product_price,
            affiliate_id=req.affiliate_id,
            affiliate_name=req.affiliate_name
        )
        if elements:
            dashboard = elements.get("simulated_dashboard_snapshot", {})
            report = booster.generate_affiliate_report(req.product_id, req.affiliate_id, dashboard, elements)
            # --- Export to Google Sheets ---
            try:
                export_to_google_sheets(GOOGLE_SHEET_ID, [
                    elements.get('product_id'),
                    elements.get('affiliate_id'),
                    elements.get('simulated_earnings_from_snapshot'),
                    elements.get('simulated_referral_percentage'),
                    elements.get('setup_timestamp_simulated'),
                    dashboard.get('fraud_flag')
                ])
            except Exception as e:
                print(f"[Google Sheets] Export failed: {e}")
            # --- Export to Airtable ---
            try:
                export_to_airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, elements)
            except Exception as e:
                print(f"[Airtable] Export failed: {e}")
            results.append({"elements": elements, "report": report})
    # --- Trigger Zapier webhook for batch ---
    try:
        trigger_zapier_webhook({"event": "batch_simulation_complete", "batch_size": len(results)})
    except Exception as e:
        print(f"[Zapier] Trigger failed: {e}")
    return {"results": results}
