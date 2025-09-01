from fastapi import APIRouter
from app.schemas.tag import TagCreate, TagRead
from app.services.tag_service import TagService
from typing import List

router = APIRouter(prefix="/tags", tags=["tags"])
tag_service = TagService()

@router.post("/", response_model=TagRead)
async def create_tag(tag: TagCreate):
    return await tag_service.tag_repo.get_or_create(tag.name)

@router.get("/", response_model=List[TagRead])
async def list_tags():
    return await tag_service.list_tags()
