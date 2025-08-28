from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.jwt import decode_token
from app.services.auth_service import is_token_blacklisted

router = APIRouter()

async def get_current_user(token: str = None, db: AsyncSession = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    payload = decode_token(token)
    if not payload or await is_token_blacklisted(db, token):
        raise HTTPException(status_code=401, detail="Invalid or blacklisted token")

    return payload["sub"]

@router.get("/me")
async def read_me(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}
