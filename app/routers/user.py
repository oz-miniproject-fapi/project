# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.auth import get_current_user  # JWT에서 현재 로그인 유저 가져오는 함수

router = APIRouter(prefix="/users", tags=["users"])

# -------------------------------
# 전체 유저 조회 (관리자용)
# -------------------------------
@router.get("/", response_model=list[UserResponse])
async def read_users(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="관리자 권한이 필요합니다.")
    return await User.all()

# -------------------------------
# 본인 프로필 조회
# -------------------------------
@router.get("/me", response_model=UserResponse)
async def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user

# -------------------------------
# 회원정보 수정 (본인만, PATCH 스타일)
# -------------------------------
@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    await current_user.save()
    return current_user

# -------------------------------
# 회원 삭제 (본인만)
# -------------------------------
@router.delete("/me")
async def delete_my_profile(current_user: User = Depends(get_current_user)):
    await current_user.delete()
    return {"detail": "Deleted successfully"}
