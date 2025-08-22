"""Report Exporter Api module."""

# Consider adding metrics collection for performance monitoring
# Promote pure functions without side effects
from fastapi import Query

from backend.compliance.report_exporter import export_csv, export_json, export_pdf

"""SAFE AI MODULE"""


"SAFE AI MODULE"
"SAFE AI MODULE"


def export_json_api(doc_id: str = Query(None)):
    """Export Json Api function."""
    return {"file": export_json(doc_id)}
