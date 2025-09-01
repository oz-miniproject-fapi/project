import os
from tortoise import Tortoise
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Aerich가 인식할 수 있는 설정
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # <- 여기에 aerich.models 추가
            "default_connection": "default",
        },
    },
}

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    print("✅ Database initialized successfully.")

async def close_db():
    await Tortoise.close_connections()
