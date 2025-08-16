"""SAFE AI MODULE"""

import json

report = {}  # TODO: Define report

"SAFE AI MODULE"
"SAFE AI MODULE"
from fastapi import Query
from backend.compliance.report_exporter import export_csv, export_json, export_pdf


def export_json_api(doc_id: str = Query(None)):
    return {"file": export_json(doc_id)}


def export_csv_api(doc_id: str = Query(None)):
    return {"file": export_csv(doc_id)}


def export_pdf_api(doc_id: str = Query(None)):
    return export_pdf(doc_id)
