# backend/routes/bobby_route.py

from fastapi import APIRouter, Request
from backend.agents.bobby import handle_bobby

router = APIRouter()


@router.post("/bobby")
async def bobby_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_bobby(user_input)
    return {"response": response}
