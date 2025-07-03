from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
import traceback
from autonomy.product_prep.gumroad_delivery import push_vault_to_gumroad, GumroadDeliveryError

router = APIRouter()

@router.post("/gumroad-deliver")
async def gumroad_deliver(request: Request):
    try:
        data = await request.json()
        metadata_path = data.get("metadataPath")
        preview_path = data.get("previewPath")
        # Optional: file_path for PDF/ZIP delivery
        file_path = data.get("filePath")
        product_id = push_vault_to_gumroad(metadata_path, preview_path, file_path)
        return JSONResponse({"success": True, "productId": product_id})
    except GumroadDeliveryError as e:
        return JSONResponse({"success": False, "error": str(e)})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e), "trace": traceback.format_exc()})
