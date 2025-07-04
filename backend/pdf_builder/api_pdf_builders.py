from fastapi import APIRouter, Depends, HTTPException
from backend.pdf_builder.expanded_pdf_builders import (
    build_niche_product_pdf,
    build_affiliate_promo_pack_pdf,
    build_social_media_content_pdf,
    build_market_trends_pdf,
    build_revenue_conversion_pdf,
    build_customer_welcome_pdf,
    build_niche_authority_ebook,
    build_email_funnel_blueprint_pdf
)
from backend.auth.deps import get_current_user
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(prefix="/pdf", tags=["PDF Builders"])

class PDFGenRequest(BaseModel):
    data: Dict[str, Any]

@router.post("/niche-product", response_model=str)
def api_niche_product_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_niche_product_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/affiliate-promo", response_model=str)
def api_affiliate_promo_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_affiliate_promo_pack_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/social-media", response_model=str)
def api_social_media_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_social_media_content_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/market-trends", response_model=str)
def api_market_trends_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_market_trends_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/revenue-conversion", response_model=str)
def api_revenue_conversion_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_revenue_conversion_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/customer-welcome", response_model=str)
def api_customer_welcome_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_customer_welcome_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/niche-ebook", response_model=str)
def api_niche_ebook_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_niche_authority_ebook(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/email-funnel-blueprint", response_model=str)
def api_email_funnel_blueprint_pdf(req: PDFGenRequest, user: str = Depends(get_current_user)):
    try:
        return build_email_funnel_blueprint_pdf(req.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
