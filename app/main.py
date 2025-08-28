# app/main.py
from fastapi import FastAPI
from app.db.database import init_db, close_db
from app.routers import user, auth

app = FastAPI(title="My FastAPI App")

# 앱 시작 시 DB 연결
@app.on_event("startup")
async def startup_event():
    await init_db()

# 앱 종료 시 DB 연결 종료
@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# 라우터 등록
app.include_router(user.router)
app.include_router(auth.router)
