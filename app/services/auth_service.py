from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from passlib.context import CryptContext
from datetime import timedelta
from app.utils.jwt import create_access_token
from tortoise.exceptions import DoesNotExist
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

class AuthService:
    def hash_password(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    async def register_user(self, email: str, password: str, nickname: str = None, phone: str = None):
        hashed_password = self.hash_password(password)
        return await User.create(email=email, password=hashed_password, nickname=nickname, phone=phone)

    async def login(self, email: str, password: str):
        try:
            user = await User.get(email=email)
        except DoesNotExist:
            raise ValueError("Invalid credentials")

        if not self.verify_password(password, user.password):
            raise ValueError("Invalid credentials")

        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta_minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta_minutes=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60
        )
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    async def logout(self, token: str):
        await TokenBlacklist.create(token=token)
