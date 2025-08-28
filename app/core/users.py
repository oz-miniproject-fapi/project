from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserCreate, UserRead, UserUpdate
from app.db.session import async_session_maker

SECRET = "YOUR_SECRET_KEY"

# DB 연결
async def get_user_db():
    async with async_session_maker() as session:
        yield SQLAlchemyUserDatabase(User, session)

# JWT 인증
auth_backends = [JWTAuthentication(secret=SECRET, lifetime_seconds=3600)]

fastapi_users = FastAPIUsers(
    get_user_db,
    auth_backends,
    User,
    UserCreate,
    UserRead,
    UserUpdate
)
