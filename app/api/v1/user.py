from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserProfileResponse, UserUpdateRequest, UserDeleteResponse
from app.services.user_service import UserService
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/api/v1/user", tags=["user"])

# --- 내 프로필 조회 ---
@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: int = Depends(get_current_user)):
    service = UserService(None)
    try:
        return await service.get_profile(current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- 내 정보 수정 (PATCH 사용) ---
@router.patch("/me", response_model=UserProfileResponse)
async def update_user(data: UserUpdateRequest, current_user: int = Depends(get_current_user)):
    service = UserService(None)
    try:
        return await service.update_user(current_user, data.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- 내 계정 삭제 ---
@router.delete("/me", response_model=UserDeleteResponse)
async def delete_user(current_user: int = Depends(get_current_user)):
    service = UserService(None)
    try:
        return await service.delete_user(current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
