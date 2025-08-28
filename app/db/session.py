# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://admin:admin1@localhost:5432/fastapi_db"

engine = create_async_engine(DATABASE_URL, echo=True)

# async_session_maker 생성
async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

# get_db 의존성
async def get_db():
    async with async_session_maker() as session:
        yield session
