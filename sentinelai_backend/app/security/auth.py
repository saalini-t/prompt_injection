from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "sentinelai-secret"
ALGORITHM = "HS256"

def create_token(username: str, role: str):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
