from fastapi import APIRouter, HTTPException, Request
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()

@router.post("/register")
async def register(email: str, password: str, nickname: str = None, phone: str = None):
    user = await auth_service.register_user(email, password, nickname, phone)
    return {
        "id": user.id,
        "email": user.email,
        "nickname": user.nickname,
        "phone": user.phone,
    }

@router.post("/login")
async def login(email: str, password: str):
    try:
        tokens = await auth_service.login(email, password)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token required")
    await auth_service.logout(token.split(" ")[1])
    return {"message": "Logged out successfully"}
