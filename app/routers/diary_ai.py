from fastapi import APIRouter

router = APIRouter()

@router.get("/diary_ai")
async def diary_ai_test():
    return {"message": "Diary AI route"}
