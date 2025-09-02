import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1 import diary, auth, user, tag
from app.db.database import init_db, close_db

# 절대경로로 .env 로드
load_dotenv("/.env")

print("GEMINI_API_KEY_PATH:", os.getenv("GEMINI_API_KEY_PATH"))  # 확인용 출력

app = FastAPI(title="Diary API")

# DB 연결
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users/api/v1", tags=["users"])
#app.include_router(diary.router, tags=["diaries"])
#app.include_router(tag.router, prefix="/tags", tags=["tags"])
