from tortoise.exceptions import DoesNotExist
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "abfadd5caf9a2d271dc0287893f31c2907de4aef1c16c8ac6f2d63b2e7395aba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    # 비밀번호 해싱/검증
    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    # JWT 생성
    def create_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # 회원가입 (phone 파라미터 추가)
    async def register_user(self, email: str, password: str, nickname: str = None, phone: str = None):
        hashed_password = self.hash_password(password)
        user = await User.create(email=email, password=hashed_password, nickname=nickname, phone=phone)
        return user

    # 로그인
    async def login(self, email: str, password: str):
        try:
            user = await User.get(email=email)
        except DoesNotExist:
            raise ValueError("Invalid credentials")

        if not self.verify_password(password, user.password):
            raise ValueError("Invalid credentials")

        access_token = self.create_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = self.create_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    # 로그아웃 (Refresh Token 블랙리스트)
    async def logout(self, token: str):
        await TokenBlacklist.create(token=token)
