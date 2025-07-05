from fastapi import APIRouter
from backend.ai.compliance_feed import fetch_compliance_feeds

router = APIRouter()


@router.get("/api/compliance/feeds")
def get_compliance_feeds():
    return fetch_compliance_feeds()
