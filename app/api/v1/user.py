from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserProfileResponse, UserUpdateRequest, UserDeleteResponse
from app.services.user_service import UserService
from app.core.auth import get_current_user
from app.models import User

router = APIRouter()  # prefix 제거, tags 제거

# --- 내 프로필 조회 ---
@router.get("/me", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    service = UserService()
    try:
        user = await service.get_profile(current_user)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- 내 정보 수정 ---
@router.patch("/me", response_model=UserProfileResponse)
async def update_user(data: UserUpdateRequest, current_user: User = Depends(get_current_user)):
    service = UserService()
    try:
        updated_user = await service.update_user(current_user, data.dict(exclude_unset=True))
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- 내 계정 삭제 ---
@router.delete("/me", response_model=UserDeleteResponse)
async def delete_user(current_user: User = Depends(get_current_user)):
    service = UserService()
    try:
        result = await service.delete_user(current_user)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
