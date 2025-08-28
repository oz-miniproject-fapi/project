# app/core/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.core.jwt import decode_token as decode_access_token  # alias 사용

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 블랙리스트 확인 (비동기)
async def is_blacklisted(token: str) -> bool:
    db_token = await TokenBlacklist.get_or_none(token=token)
    return db_token is not None

# 현재 로그인 사용자 가져오기
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    if await is_blacklisted(token):
        raise HTTPException(status_code=401, detail="블랙리스트에 등록된 토큰입니다.")

    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

    user = await User.get_or_none(id=payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="비활성 회원이거나 존재하지 않는 사용자입니다.")

    return user

# 관리자 권한 체크
async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")
    return user
