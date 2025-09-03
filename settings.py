import os

POSTGRES_USER = os.getenv("POSTGRES_USER", "admin1")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin1")
POSTGRES_DB = os.getenv("POSTGRES_DB", "fastapi_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# 최신 Tortoise ORM + PostgreSQL 드라이버 호환
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Tortoise ORM 설정
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
