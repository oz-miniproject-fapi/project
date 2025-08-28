from fastapi import APIRouter

router = APIRouter()

@router.get("/diaries")
async def read_diaries():
    return {"message": "다이어리 리스트"}
