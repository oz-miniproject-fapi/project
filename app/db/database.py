import os
from tortoise import Tortoise
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

DB_URL = (
    f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    }
}

# DB 초기화
async def init_db():
    await Tortoise.init(db_url=DB_URL, modules={"models": ["app.models"]})
    await Tortoise.generate_schemas()
    print(" Database initialized successfully.")

# DB 종료
async def close_db():
    await Tortoise.close_connections()

# get_db (ImportError 방지용)
async def get_db():
    yield  # Tortoise ORM은 세션 yield 필요 없음
