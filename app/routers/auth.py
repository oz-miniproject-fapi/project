# app/routers/auth.py
from fastapi import APIRouter, Response, HTTPException, status
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.core.jwt import create_access_token, create_refresh_token, create_email_token, decode_email_token
from app.utils.email import send_verification_email

router = APIRouter()

# -------------------------------
# 회원가입
# -------------------------------
@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(signup_data: SignupRequest):
    # 유저 생성
    user = await User.create(
        email=signup_data.email,
        nickname=signup_data.nickname,
        name=signup_data.name,
        phone_number=signup_data.phone_number,
        is_active=False  # 이메일 인증 전 비활성화
    )
    # 비밀번호 해시 저장
    user.set_password(signup_data.password)
    await user.save()

    # 이메일 인증 토큰 생성 및 발송
    token = create_email_token({"sub": str(user.id)})
    await send_verification_email(user.email, token)

    return {"access_token": "", "refresh_token": "", "token_type": "bearer"}

# -------------------------------
# 이메일 인증
# -------------------------------
@router.get("/verify-email")
async def verify_email(token: str):
    payload = decode_email_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await User.get_or_none(id=int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True
    await user.save()
    return {"detail": "Email verified successfully. You can now log in."}

# -------------------------------
# 로그인
# -------------------------------
@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, response: Response):
    user = await User.get_or_none(email=login_data.email)
    if not user or not user.verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Email not verified")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # 쿠키에 액세스 토큰 저장
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=3600,
        samesite="lax"
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# -------------------------------
# 로그아웃
# -------------------------------
@router.post("/logout")
async def logout(refresh_token: str, response: Response):
    # 토큰 블랙리스트에 저장
    await TokenBlacklist.create(token=refresh_token)

    # 쿠키 삭제
    response.delete_cookie("access_token")
    return {"detail": "Successfully logged out"}
