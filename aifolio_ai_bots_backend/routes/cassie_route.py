# backend/routes/cassie_route.py

from fastapi import APIRouter, Request
from backend.agents.cassie import handle_cassie

router = APIRouter()

@router.post("/cassie")
async def cassie_endpoint(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    response = handle_cassie(user_input)
    return {"response": response}
