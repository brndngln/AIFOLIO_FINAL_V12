from fastapi import APIRouter, Query
from backend.compliance.report_exporter import export_json, export_csv, export_pdf

router = APIRouter()

@router.get('/api/report/export_json')
def export_json_api(doc_id: str = Query(None)):
    return {'file': export_json(doc_id)}

@router.get('/api/report/export_csv')
def export_csv_api(doc_id: str = Query(None)):
    return {'file': export_csv(doc_id)}

@router.get('/api/report/export_pdf')
def export_pdf_api(doc_id: str = Query(None)):
    return export_pdf(doc_id)
