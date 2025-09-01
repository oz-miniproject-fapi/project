from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import TokenBlacklist

class TokenBlacklistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, token: str):
        token_entry = TokenBlacklist(token=token)
        self.db.add(token_entry)
        await self.db.commit()
        return token_entry

    async def exists(self, token: str):
        result = await self.db.execute(
            select(TokenBlacklist).where(TokenBlacklist.token == token)
        )
        return result.scalars().first() is not None
