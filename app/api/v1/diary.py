from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import date
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.services.diary_service import DiaryService
from app.models.user import User
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/diaries", tags=["diaries"])

# --- CRUD + 태그 포함 ---
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary: DiaryCreate, current_user: User = Depends(get_current_user)):
    return await DiaryService.create_diary_with_tags(
        user_id=current_user.id,
        title=diary.title,
        content=diary.content,
        tag_names=diary.tags
    )

@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryService.get_diary(current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return DiaryResponse(
        id=diary.id,
        title=diary.title,
        content=diary.content,
        tags=[tag.name for tag in diary.tags],
        emotion=diary.emotion,
        emotion_keywords=[{"word": kw.word, "emotion": kw.emotion} for kw in getattr(diary, "emotion_keywords", [])],
        created_at=diary.created_at,
        updated_at=diary.updated_at
    )

@router.get("/", response_model=List[DiaryResponse])
async def list_diaries(oldest_first: Optional[bool] = False, current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.list_diaries(current_user.id, oldest_first)
    return [
        DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=d.emotion,
            emotion_keywords=[{"word": kw.word, "emotion": kw.emotion} for kw in getattr(d, "emotion_keywords", [])],
            created_at=d.created_at,
            updated_at=d.updated_at
        )
        for d in diaries
    ]

@router.put("/{diary_id}", response_model=DiaryResponse)
async def update_diary(diary_id: int, diary_update: DiaryUpdate, current_user: User = Depends(get_current_user)):
    diary = await DiaryService.get_diary(current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    updated_diary = await DiaryService.update_diary_with_tags(
        diary,
        title=diary_update.title,
        content=diary_update.content,
        tag_names=diary_update.tags
    )
    return DiaryResponse(
        id=updated_diary.id,
        title=updated_diary.title,
        content=updated_diary.content,
        tags=[tag.name for tag in updated_diary.tags],
        emotion=updated_diary.emotion,
        emotion_keywords=[{"word": kw.word, "emotion": kw.emotion} for kw in getattr(updated_diary, "emotion_keywords", [])],
        created_at=updated_diary.created_at,
        updated_at=updated_diary.updated_at
    )

@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryService.get_diary(current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    await DiaryService.delete_diary(diary)
    return {"detail": "Diary deleted"}

# --- 검색 ---
@router.get("/search", response_model=List[DiaryResponse])
async def search_diaries(title: Optional[str] = None, diary_date: Optional[date] = None,
                          oldest_first: Optional[bool] = False, current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.search_diaries(current_user.id, title, diary_date, oldest_first)
    return [
        DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=d.emotion,
            emotion_keywords=[{"word": kw.word, "emotion": kw.emotion} for kw in getattr(d, "emotion_keywords", [])],
            created_at=d.created_at,
            updated_at=d.updated_at
        )
        for d in diaries
    ]

# --- 태그 필터링 ---
@router.get("/tag/{tag_name}", response_model=List[DiaryResponse])
async def get_diaries_by_tag(tag_name: str, current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.list_diaries_by_tag(current_user.id, tag_name)
    return [
        DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=d.emotion,
            emotion_keywords=[{"word": kw.word, "emotion": kw.emotion} for kw in getattr(d, "emotion_keywords", [])],
            created_at=d.created_at,
            updated_at=d.updated_at
        )
        for d in diaries
    ]

# --- AI 요약 ---
@router.post("/{diary_id}/summarize", response_model=dict)
async def summarize_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    summary = await DiaryService.summarize_diary(diary_id, current_user.id)
    if summary is None:
        raise HTTPException(status_code=404, detail="Diary not found")
    return {"diary_id": diary_id, "summary": summary}

# --- AI 감정 분석 ---
@router.post("/{diary_id}/analyze-emotions", response_model=dict)
async def analyze_emotions(diary_id: int, current_user: User = Depends(get_current_user)):
    keywords = await DiaryService.analyze_diary_emotions(diary_id, current_user.id)
    if keywords is None:
        raise HTTPException(status_code=404, detail="Diary not found")
    return {"diary_id": diary_id, "emotion_keywords": keywords}
