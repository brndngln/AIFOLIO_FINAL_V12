# backend/routes/victor_route.py

from fastapi import APIRouter, Request
from backend.agents.victor import handle_victor

router = APIRouter()

@router.post("/victor")
async def victor_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_victor(user_input)
    return {"response": response}
