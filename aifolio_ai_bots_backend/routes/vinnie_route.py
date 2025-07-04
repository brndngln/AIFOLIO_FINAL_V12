# backend/routes/vinnie_route.py

from fastapi import APIRouter, Request
from backend.agents.vinnie import handle_vinnie

router = APIRouter()

@router.post("/vinnie")
async def vinnie_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_vinnie(user_input)
    return {"response": response}
