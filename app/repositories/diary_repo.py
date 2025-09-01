from app.models.diary import Diary
from app.models.diary_tag import DiaryTag

class DiaryRepository:
    async def create(self, user, data):
        return await Diary.create(user=user, title=data["title"], content=data["content"])

    async def get_by_id(self, diary_id: int):
        return await Diary.get_or_none(id=diary_id)

    async def update(self, diary_id: int, **kwargs):
        diary = await Diary.get_or_none(id=diary_id)
        if not diary:
            return None
        for key, value in kwargs.items():
            setattr(diary, key, value)
        await diary.save()
        return diary

    async def delete(self, diary_id: int):
        diary = await Diary.get_or_none(id=diary_id)
        if diary:
            await diary.delete()
            return True
        return False

    async def add_tag(self, diary, tag):
        await DiaryTag.create(diary=diary, tag=tag)
