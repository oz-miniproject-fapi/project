# app/utils/jwt.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt

# 사용자 제공 SECRET_KEY
SECRET_KEY = "abfadd5caf9a2d271dc0287893f31c2907de4aef1c16c8ac6f2d63b2e7395aba"
ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(token: str = Depends(security)):
    """
    JWT Access Token을 검증하고 user_id 반환
    """
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
