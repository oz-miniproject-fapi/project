from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from app.models.user import User

SECRET_KEY = "abfadd5caf9a2d271dc0287893f31c2907de4aef1c16c8ac6f2d63b2e7395aba"
ALGORITHM = "HS256"

security = HTTPBearer()

def decode_access_token(token: str) -> dict:
    """
    JWT Access Token 디코딩
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(token: str = Depends(security)) -> User:
    """
    JWT Access Token 검증 후 User 객체 반환
    """
    payload = decode_access_token(token.credentials)
    user_id = int(payload.get("sub"))
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
