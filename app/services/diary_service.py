from app.models.diary import Diary, Tag
from app.models.user import User
from tortoise.exceptions import DoesNotExist
from typing import Optional

class DiaryService:

    @staticmethod
    async def create_diary(user: User, data: dict):
        return await Diary.create(user=user, **data)

    @staticmethod
    async def get_diaries(user: User, title: Optional[str] = None, date: Optional[str] = None,
                          sort: str = "desc", tag_id: Optional[int] = None):
        query = Diary.filter(user=user)
        if title:
            query = query.filter(title__icontains=title)
        if date:
            query = query.filter(created_at__date=date)
        if tag_id:
            tag = await Tag.get_or_none(id=tag_id)
            if not tag:
                raise DoesNotExist("Tag not found")
            query = query.filter(tags__id=tag_id)
        query = query.order_by("created_at" if sort=="asc" else "-created_at")
        return await query
