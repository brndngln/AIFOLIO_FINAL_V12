# backend/routes/emmi_route.py

from fastapi import APIRouter, Request
from backend.agents.emmi import handle_emmi

router = APIRouter()

@router.post("/emmi")
async def emmi_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_emmi(user_input)
    return {"response": response}
