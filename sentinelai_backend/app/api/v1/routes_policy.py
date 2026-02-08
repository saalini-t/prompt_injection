from fastapi import APIRouter
from app.security.auth import create_token

router = APIRouter()

@router.post("/login")
def login(payload: dict):
    # demo users
    users = {"admin":"admin123", "analyst":"analyst123"}

    if payload["username"] in users and payload["password"] == users[payload["username"]]:
        role = payload["username"]
        return {"token": create_token(payload["username"], role)}

    return {"error":"Invalid credentials"}
