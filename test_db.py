import asyncio
from app.db.database import init_db, close_db

async def test():
    await init_db()
    await close_db()

asyncio.run(test())
