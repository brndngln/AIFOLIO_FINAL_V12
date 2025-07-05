# backend/routes/barbara_route.py

from fastapi import APIRouter, Request
from backend.agents.barbara import handle_barbara

router = APIRouter()


@router.post("/barbara")
async def barbara_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_barbara(user_input)
    return {"response": response}
