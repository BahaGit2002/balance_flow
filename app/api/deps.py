from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config.security import decode_jwt

security = HTTPBearer()


def get_current_user(credential: HTTPAuthorizationCredentials = Depends(security)):
    token = credential.credentials
    payload = decode_jwt(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )
    return payload
