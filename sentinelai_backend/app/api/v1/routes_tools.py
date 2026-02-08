from fastapi import APIRouter, Request
from app.gateway.tool_middleware import tool_firewall

router = APIRouter()

@router.post("/execute")
def execute_tool(request: Request, payload: dict):

    tool = payload["tool"]
    decision = payload["policy"]

    tool_firewall(request, tool, decision)

    return {"status": "Tool executed safely", "tool": tool}
