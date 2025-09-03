from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.diary import DiaryCreate, DiaryUpdate, DiaryResponse
from app.services.diary_service import DiaryService
from app.models.user import User
from app.core.auth import get_current_user

# 🔹 prefix 제거 → main.py에서 /api/v1/diaries 적용
router = APIRouter(tags=["diaries"])

# -------------------
# 1. 다이어리 생성
# -------------------
@router.post("/", response_model=DiaryResponse)
async def create_diary(diary: DiaryCreate, current_user: User = Depends(get_current_user)):
    created_diary = await DiaryService.create_diary_with_tags(
        user_id=current_user.id,
        title=diary.title,
        content=diary.content,
        tag_names=diary.tags
    )
    await created_diary.fetch_related("tags")
    return DiaryResponse(
        id=created_diary.id,
        title=created_diary.title,
        content=created_diary.content,
        tags=[tag.name for tag in created_diary.tags],
        emotion=None,
        emotion_keywords=[],
        created_at=created_diary.created_at,
        updated_at=created_diary.updated_at
    )

# -------------------
# 2. 키워드 기반 검색
# -------------------
@router.get("/search", response_model=List[DiaryResponse])
async def search_diaries(
    keyword: str = Query(..., description="검색할 키워드"),
    current_user: User = Depends(get_current_user)
):
    diaries = await DiaryService.search_diaries(current_user.id, keyword)
    return [
        DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=None,
            emotion_keywords=[],
            created_at=d.created_at,
            updated_at=d.updated_at
        )
        for d in diaries
    ]

# -------------------
# 3. 태그 기반 조회 (최대 10개)
# -------------------
@router.get("/tag/{tag_name}", response_model=List[DiaryResponse])
async def get_diaries_by_tag(tag_name: str, current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.list_diaries_by_tag(current_user.id, tag_name, limit=10)
    return [
        DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=None,
            emotion_keywords=[],
            created_at=d.created_at,
            updated_at=d.updated_at
        )
        for d in diaries
    ]

# -------------------
# 4. 단일 다이어리 조회
# -------------------
@router.get("/{diary_id}", response_model=DiaryResponse)
async def get_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryService.get_diary(current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    await diary.fetch_related("tags")
    return DiaryResponse(
        id=diary.id,
        title=diary.title,
        content=diary.content,
        tags=[tag.name for tag in diary.tags],
        emotion=None,
        emotion_keywords=[],
        created_at=diary.created_at,
        updated_at=diary.updated_at
    )

# -------------------
# 5. 전체 다이어리 목록 조회
# -------------------
@router.get("/", response_model=List[DiaryResponse])
async def list_diaries(oldest_first: Optional[bool] = False, current_user: User = Depends(get_current_user)):
    diaries = await DiaryService.list_diaries(current_user.id, oldest_first)
    results = []
    for d in diaries:
        await d.fetch_related("tags")
        results.append(DiaryResponse(
            id=d.id,
            title=d.title,
            content=d.content,
            tags=[tag.name for tag in d.tags],
            emotion=None,
            emotion_keywords=[],
            created_at=d.created_at,
            updated_at=d.updated_at
        ))
    return results

# -------------------
# 6. 다이어리 수정
# -------------------
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
    await updated_diary.fetch_related("tags")
    return DiaryResponse(
        id=updated_diary.id,
        title=updated_diary.title,
        content=updated_diary.content,
        tags=[tag.name for tag in updated_diary.tags],
        emotion=None,
        emotion_keywords=[],
        created_at=updated_diary.created_at,
        updated_at=updated_diary.updated_at
    )

# -------------------
# 7. 다이어리 삭제
# -------------------
@router.delete("/{diary_id}")
async def delete_diary(diary_id: int, current_user: User = Depends(get_current_user)):
    diary = await DiaryService.get_diary(current_user.id, diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    await DiaryService.delete_diary(diary)
    return {"detail": "Diary deleted"}

# -------------------
# 8. AI 관련 기능 (주석 처리)
# -------------------
# @router.post("/{diary_id}/summarize", response_model=dict)
# async def summarize_diary(diary_id: int, current_user: User = Depends(get_current_user)):
#     summary = await DiaryService.summarize_diary(diary_id, current_user.id)
#     if summary is None:
#         raise HTTPException(status_code=404, detail="Diary not found")
#     return {"diary_id": diary_id, "summary": summary}

# @router.post("/{diary_id}/analyze-emotions", response_model=dict)
# async def analyze_emotions(diary_id: int, current_user: User = Depends(get_current_user)):
#     keywords = await DiaryService.analyze_diary_emotions(diary_id, current_user.id)
#     if keywords is None:
#         raise HTTPException(status_code=404, detail="Diary not found")
#     return {"diary_id": diary_id, "emotion_keywords": keywords}
