from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 회원가입
class UserSignupRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None
    phone: Optional[str] = None

class UserSignupResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime]

# 로그인
class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# 로그아웃
class UserLogoutRequest(BaseModel):
    refresh_token: str

class UserLogoutResponse(BaseModel):
    message: str = "Logout successful"
