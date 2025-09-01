from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- 사용자 정보 조회 ---
class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

# --- 사용자 정보 수정 ---
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None

# --- 사용자 삭제 응답 ---
class UserDeleteResponse(BaseModel):
    message: str = Field(default="Deleted successfully")
