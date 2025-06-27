from fastapi import APIRouter, Body
from backend.compliance.violation_engine import scan_pdf_text, log_violations, get_violations

router = APIRouter()

@router.post('/api/compliance/scan_pdf')
def scan_pdf(data: dict = Body(...)):
    text = data.get('text')
    platforms = data.get('platforms')
    doc_id = data.get('doc_id')
    detected_by = data.get('detected_by')
    violations = scan_pdf_text(text, platforms)
    logged = log_violations(doc_id, violations, detected_by)
    return {'violations': logged}

@router.get('/api/compliance/violations')
def violations(doc_id: str = None, status: str = None):
    return get_violations(doc_id, status)
