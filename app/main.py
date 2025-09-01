from fastapi import FastAPI
from app.api.v1 import auth, user  # user 라우터 추가
from app.db.database import init_db, close_db

app = FastAPI(title="FastAPI JWT Auth Example")

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# 라우터 등록
app.include_router(auth.router)
app.include_router(user.router)  # user 라우터 등록
