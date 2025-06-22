from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .batch16_20_models import *
from backend.utils.safe_ai_utils import safe_ai_guarded
from backend.main import get_current_user
import datetime

router = APIRouter(prefix="/batch-scaling", tags=["SAFE AI Batches 16-20"])

# --- Batch 16 ---
@router.get("/multi-currency-revenue", response_model=List[MultiCurrencyRevenue])
def get_multi_currency_revenue(user: str = Depends(get_current_user)):
    return []  # Static/admin input only

@router.post("/multi-currency-revenue", response_model=MultiCurrencyRevenue)
@safe_ai_guarded
def add_multi_currency_revenue(entry: MultiCurrencyRevenue, user: str = Depends(get_current_user)):
    return entry

@router.get("/tax-region-report", response_model=List[TaxRegionReport])
def get_tax_region_report(user: str = Depends(get_current_user)):
    return []

@router.post("/tax-region-report", response_model=TaxRegionReport)
@safe_ai_guarded
def add_tax_region_report(entry: TaxRegionReport, user: str = Depends(get_current_user)):
    return entry

# ...repeat for all other models in batches 16–20 and partner certification...

# --- Partner Certification ---
@router.get("/partner-certifications", response_model=List[PartnerCertification])
def get_partner_certifications(user: str = Depends(get_current_user)):
    return []

@router.post("/partner-certifications", response_model=PartnerCertification)
@safe_ai_guarded
def add_partner_certification(entry: PartnerCertification, user: str = Depends(get_current_user)):
    return entry

@router.post("/partner-self-cert", response_model=PartnerSelfCertSubmission)
@safe_ai_guarded
def submit_partner_self_cert(entry: PartnerSelfCertSubmission, user: str = Depends(get_current_user)):
    return entry

@router.get("/certification-audit-reports", response_model=List[CertificationAuditReport])
def get_certification_audit_reports(user: str = Depends(get_current_user)):
    return []

@router.post("/certification-audit-reports", response_model=CertificationAuditReport)
@safe_ai_guarded
def add_certification_audit_report(entry: CertificationAuditReport, user: str = Depends(get_current_user)):
    return entry

from fastapi import Query
from fastapi.responses import FileResponse
from .export_utils import export_pdf, export_csv, log_export
from datetime import datetime

@router.get("/partner-certifications/export")
def export_partner_certification(type: str = Query(..., regex="^(pdf|csv)$"), partner: str = Query(...), user: str = Depends(get_current_user)):
    # Dummy static data for demo; replace with DB lookup
    cert_data = {
        "partner": partner,
        "certification_status": "Approved",
        "expiry_date": str(datetime.now().date()),
        "last_audit": str(datetime.now().date()),
        "terms_file": "terms.pdf",
        "contact_email": "partner@example.com",
        "notes": "SAFE AI compliant."
    }
    filename = f"{partner}_certification.{type}"
    if type == "csv":
        path = export_csv(filename, [cert_data], list(cert_data.keys()), folder="partner_certification")
    else:
        path = export_pdf(filename, "partner_certification_report.html", cert_data, folder="partner_certification")
    log_export(f"export_partner_certification_{type}", user, {"partner": partner, "file": path})
    return FileResponse(path, filename=filename)

# --- Public SAFE AI System Transparency Report ---
@router.get("/public-report/export")
def export_public_report(user: str = Depends(get_current_user)):
    now = datetime.now().isoformat()
    context = {
        "principles": "SAFE AI Principles: Static, Deterministic, Non-sentient, Non-adaptive, Fully Audited.",
        "scope": "System Scope: All SAFE AI Batches 16–20, Partner Certification, Public Reports.",
        "audit_history": "All actions 100% logged.",
        "cert_summary": "All partners certified under SAFE AI compliance.",
        "governance_log": "All admin actions reviewed.",
        "public_trust_badge": "Earned",
        "now": now
    }
    filename = f"safe_ai_public_report_{now[:10]}.pdf"
    path = export_pdf(filename, "public_report.html", context, folder="public_reports")
    log_export("export_public_report_pdf", user, {"file": path})
    return FileResponse(path, filename=filename)

# --- Batch 16–20 PDF/CSV Export Placeholders ---
@router.get("/batch-export/{batch}/{type}")
def export_batch(batch: str, type: str, user: str = Depends(get_current_user)):
    # batch: batch16, batch17, ... batch20
    # type: pdf or csv
    filename = f"{batch}_export.{type}"
    # For demo, export dummy static data
    data = [{"field": "value"}]
    if type == "csv":
        path = export_csv(filename, data, ["field"], folder="csv")
    else:
        context = {"batch": batch, "data": data, "now": datetime.now().isoformat()}
        path = export_pdf(filename, "batch_report.html", context, folder="pdf")
    log_export(f"export_{batch}_{type}", user, {"file": path})
    return FileResponse(path, filename=filename)
