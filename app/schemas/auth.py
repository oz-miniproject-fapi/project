# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# -------------------------------
# 회원가입 요청 (Request Body)
# -------------------------------
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    nickname: Optional[str] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None

# -------------------------------
# 회원가입 응답 (Response Body)
# -------------------------------
class SignupResponse(BaseModel):
    user_id: int
    msg: str = "회원가입이 완료되었습니다."

# -------------------------------
# 로그인 요청 (Request Body)
# -------------------------------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# -------------------------------
# 로그인 응답 (Response Body)
# -------------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# -------------------------------
# 로그아웃 요청 (Request Body)
# -------------------------------
class LogoutRequest(BaseModel):
    refresh_token: str

# -------------------------------
# 로그아웃 응답 (Response Body)
# -------------------------------
class LogoutResponse(BaseModel):
    detail: str = "Successfully logged out"
