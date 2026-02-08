from fastapi import Request, HTTPException
from app.gateway.permissions import TOOL_PERMISSIONS

def tool_firewall(request: Request, tool_name: str, policy_decision: dict):

    risk = TOOL_PERMISSIONS.get(tool_name, "high")

    if policy_decision["decision"] == "block":
        raise HTTPException(403, detail="Blocked by Prompt Firewall")

    if risk == "critical" and policy_decision["decision"] != "allow":
        raise HTTPException(403, detail="Critical tool access denied")

    return True
