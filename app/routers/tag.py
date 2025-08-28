# app/routers/tag.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import async_session_maker
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagRead
from typing import List

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

# DB 세션
async def get_db():
    async with async_session_maker() as session:
        yield session

# 전체 태그 조회
@router.get("/", response_model=List[TagRead])
async def get_tags(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tag))
    tags = result.scalars().all()
    return tags

# 단일 태그 조회
@router.get("/{tag_id}", response_model=TagRead)
async def get_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(Tag, tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return result

# 태그 생성
@router.post("/", response_model=TagRead)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(get_db)):
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

# 태그 삭제
@router.delete("/{tag_id}", response_model=dict)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db)):
    db_tag = await db.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await db.delete(db_tag)
    await db.commit()
    return {"message": "Tag deleted"}
