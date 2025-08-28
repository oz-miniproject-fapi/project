from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.core.jwt import create_access_token, create_refresh_token, create_email_token
from app.utils.email import send_verification_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# 유저 생성 (회원가입 + 이메일 인증)
# -------------------------------
async def create_user(db: AsyncSession, email: str, password: str, nickname: str = None, name: str = None, phone_number: str = None):
    hashed_password = pwd_context.hash(password)
    new_user = User(
        email=email,
        password=hashed_password,
        nickname=nickname,
        name=name,
        phone_number=phone_number,
        is_active=False  # 이메일 인증 전 비활성화
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 이메일 인증 토큰 생성 및 발송
    token = create_email_token({"sub": str(new_user.id)})
    await send_verification_email(new_user.email, token)

    return new_user

# -------------------------------
# 유저 인증 (로그인)
# -------------------------------
async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(password, user.password):
        return None
    if not user.is_active:
        return None  # 이메일 인증 전 로그인 불가
    return user

async def login_user(db: AsyncSession, email: str, password: str):
    user = await authenticate_user(db, email, password)
    if not user:
        return None

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "user": user}

# -------------------------------
# 토큰 블랙리스트
# -------------------------------
async def add_token_to_blacklist(db: AsyncSession, token: str):
    db_token = TokenBlacklist(token=token)
    db.add(db_token)
    await db.commit()

async def is_token_blacklisted(db: AsyncSession, token: str):
    result = await db.get(TokenBlacklist, token)
    return result is not None
