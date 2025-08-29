# app/routers/diary.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.diary import Diary
from app.models.diary_tag import DiaryTag
from app.models.diary_emotion_keyword import DiaryEmotionKeyword
from app.schemas.diary import DiaryResponse, DiaryCreate, DiaryUpdate
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/diaries", tags=["diaries"])

# -------------------------------
# 전체 일기 조회 (본인, 최신순)
# -------------------------------
@router.get("/", response_model=List[DiaryResponse])
async def read_diaries(current_user: User = Depends(get_current_user)):
    diaries = await Diary.filter(user_id=current_user.id) \
                         .prefetch_related("diary_tags", "diary_emotion_keywords") \
                         .order_by("-created_at")
    return diaries

# -------------------------------
# 일기 작성
# -------------------------------
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary_data: DiaryCreate, current_user: User = Depends(get_current_user)):
    diary = await Diary.create(
        user_id=current_user.id,
        title=diary_data.title,
        content=diary_data.content
    )
    # 태그 추가
    if diary_data.tags:
        for tag_name in diary_data.tags:
            await DiaryTag.create(diary_id=diary.id, name=tag_name)
    # 감정 키워드 자동 생성 로직은 필요 시 구현
    await diary.fetch_related("diary_tags", "diary_emotion_keywords")
    return diary

# -------------------------------
# 일기 수정 (PATCH, 본인만)
# -------------------------------
@router.patch("/{diary_id}", response_model=DiaryResponse)
async def update_diary(diary_id: int, diary_data: DiaryUpdate, current_user: User = Depends(get_current_user)):
    diary = await Diary.get_or_none(id=diary_id, user_id=current_user.id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    update_fields = diary_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(diary, field, value)
    await diary.save()

    # 태그 수정
    if diary_data.tags is not None:
        # 기존 태그 삭제
        await DiaryTag.filter(diary_id=diary.id).delete()
        # 새 태그 추가
        for tag_name in diary_data.tags:
            await DiaryTag.create(diary_id=diary.id, name=tag_name)

    await diary.fetch_related("diary_tags", "diary_emotion_keywords")
    return diary

# -------------------------------
# 일기 삭제 (본인만)
# -------------------------------
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await Diary.get_or_none(id=diary_id, user_id=current_user.id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    await diary.delete()
    return {"detail": "Deleted successfully"}
