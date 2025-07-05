# backend/routes/adam_route.py

from fastapi import APIRouter, Request
from backend.agents.adam import handle_adam

router = APIRouter()


@router.post("/adam")
async def adam_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_adam(user_input)
    return {"response": response}
