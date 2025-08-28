import asyncio
from tortoise import Tortoise

from app.db.database import TORTOISE_ORM  # 실제 DB 설정 임포트

async def test_connection():
    await Tortoise.init(config=TORTOISE_ORM)
    print("✅ DB 연결 성공")
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_connection())
