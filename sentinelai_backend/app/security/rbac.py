from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt
from app.security.auth import SECRET_KEY, ALGORITHM

security = HTTPBearer()

def require_role(required_role: str):
    def checker(token=Depends(security)):
        data = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if data["role"] != required_role:
            raise HTTPException(403, "Access denied")
        return data
    return checker
