from fastapi import FastAPI
from app.api.v1 import diary, auth, user, tag  # tag 추가
from app.db.database import init_db, close_db

app = FastAPI(title="Diary API")

# 앱 시작 시 DB 연결
@app.on_event("startup")
async def on_startup():
    await init_db()

# 앱 종료 시 DB 연결 종료
@app.on_event("shutdown")
async def on_shutdown():
    await close_db()

# 라우터 등록
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(diary.router, prefix="/diaries", tags=["diaries"])  # diary prefix 추가
app.include_router(tag.router, prefix="/tags", tags=["tags"])  # tag 라우터 등록
