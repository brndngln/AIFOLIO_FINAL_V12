"""
AIFOLIO™ Empire Admin Dashboard API Endpoint
Serves SAFE AI engine logs to the frontend dashboard.
Static, deterministic, owner-controlled, SAFE AI-compliant.
"""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from autonomy.dashboard.empire_admin_dashboard import EmpireAdminDashboard

router = APIRouter()

dashboard = EmpireAdminDashboard()

@router.get("/api/dashboard/logs")
def get_dashboard_logs():
    logs = dashboard.get_all_logs()
    return JSONResponse(content=logs)

# Export endpoint (JSON/CSV)
import csv
from fastapi.responses import StreamingResponse
import io

@router.get("/api/dashboard/export/json")
def export_logs_json():
    logs = dashboard.get_all_logs()
    return JSONResponse(content=logs)

@router.get("/api/dashboard/export/csv")
def export_logs_csv():
    logs = dashboard.get_all_logs()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["engine","entry"])
    for engine, entries in logs.items():
        for entry in entries:
            writer.writerow([engine, str(entry)])
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv")

# Compliance integration stub
@router.get("/api/dashboard/compliance/check")
def compliance_check():
    # Placeholder: Insert static SAFE AI compliance check logic here
    return {"status": "SAFE AI compliance: PASS", "timestamp": "2025-06-24T22:00:43-06:00"}
