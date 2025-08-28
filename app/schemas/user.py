from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 유저 조회용
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str]
    name: Optional[str]
    phone_number: Optional[str]
    is_staff: bool
    is_admin: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 회원정보 수정용
class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
