from typing import List, Optional
from app.models.diary import Diary, Tag, TransactionHistory
from app.models.user import User
from tortoise.exceptions import DoesNotExist

class DiaryService:

    @staticmethod
    async def create_diary(user: User, data):
        diary_obj = await Diary.create(user=user, **data)
        return diary_obj

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
        query = query.order_by("created_at" if sort == "asc" else "-created_at")
        return query

    @staticmethod
    async def get_diary(user: User, diary_id: int):
        diary = await Diary.get_or_none(id=diary_id, user=user)
        if not diary:
            raise DoesNotExist("Diary not found")
        return diary

    @staticmethod
    async def update_diary(user: User, diary_id: int, data):
        diary = await DiaryService.get_diary(user, diary_id)
        await diary.update_from_dict(data).save()
        return diary

    @staticmethod
    async def delete_diary(user: User, diary_id: int):
        diary = await DiaryService.get_diary(user, diary_id)
        await diary.delete()
        return True

    # ---------------- Tag ----------------
    @staticmethod
    async def create_tag(data):
        tag_obj = await Tag.create(**data)
        return tag_obj

    @staticmethod
    async def attach_tag(user: User, diary_id: int, tag_id: int):
        diary = await DiaryService.get_diary(user, diary_id)
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise DoesNotExist("Tag not found")
        await diary.tags.add(tag)
        return True

    @staticmethod
    async def remove_tag(user: User, diary_id: int, tag_id: int):
        diary = await DiaryService.get_diary(user, diary_id)
        tag = await Tag.get_or_none(id=tag_id)
        if not tag:
            raise DoesNotExist("Tag not found")
        await diary.tags.remove(tag)
        return True


