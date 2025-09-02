# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. .env 파일 경로 지정 및 로드
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# 2. 환경 변수 읽기
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 3. DB_PORT를 int로 변환 (없으면 기본 5432)
DB_PORT = int(DB_PORT) if DB_PORT else 5432

# 4. Tortoise ORM용 DB URL 생성
DB_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 5. Aerich가 인식할 수 있는 Tortoise ORM 설정
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],  # 프로젝트 모델 + aerich 포함
            "default_connection": "default",
        }
    },
}

# 6. 확인용 출력 (테스트용)
if __name__ == "__main__":
    print("DB_HOST:", DB_HOST)
    print("DB_PORT:", DB_PORT)
    print("DB_USER:", DB_USER)
    print("DB_NAME:", DB_NAME)
    print("DB_URL:", DB_URL)
