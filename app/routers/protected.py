# app/routers/protected.py
from fastapi import APIRouter, Depends, HTTPException
from app.models.token_blacklist import TokenBlacklist
from app.core.jwt import decode_token

router = APIRouter()

async def get_current_user(token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 블랙리스트 확인
    blacklisted = await TokenBlacklist.filter(token=token).exists()
    if blacklisted:
        raise HTTPException(status_code=401, detail="Token is blacklisted")

    return payload["sub"]

@router.get("/me")
async def read_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
