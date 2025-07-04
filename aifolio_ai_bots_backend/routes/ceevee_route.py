# backend/routes/ceevee_route.py

from fastapi import APIRouter, Request
from backend.agents.ceevee import handle_ceevee

router = APIRouter()

@router.post("/ceevee")
async def ceevee_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_ceevee(user_input)
    return {"response": response}
