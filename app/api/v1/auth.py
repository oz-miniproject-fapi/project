from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService
from app.schemas.auth import (
    UserSignupRequest, UserSignupResponse,
    UserLoginRequest, UserLoginResponse,
    UserLogoutRequest, UserLogoutResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register", response_model=UserSignupResponse)
async def register(data: UserSignupRequest):
    user = await auth_service.register_user(
        email=data.email,
        password=data.password,
        nickname=data.nickname,
        phone=data.phone
    )
    return {
        "id": user.id,
        "email": user.email,
        "nickname": user.nickname,
        "name": getattr(user, "name", None),
        "phone": user.phone,
        "created_at": getattr(user, "created_at", None)
    }

@router.post("/login", response_model=UserLoginResponse)
async def login(data: UserLoginRequest):
    try:
        tokens = await auth_service.login(email=data.email, password=data.password)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout", response_model=UserLogoutResponse)
async def logout(data: UserLogoutRequest):
    try:
        await auth_service.logout(data.refresh_token)
        return {"message": "Logout successful"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
