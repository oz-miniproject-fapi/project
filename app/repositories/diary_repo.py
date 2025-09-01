from app.models.diary import Diary

class DiaryRepository:
    @staticmethod
    async def create_diary(user_id: int, title: str, content: str):
        return await Diary.create(user_id=user_id, title=title, content=content)

    @staticmethod
    async def get_diary_by_id(user_id: int, diary_id: int):
        return await Diary.get(id=diary_id, user_id=user_id)

    @staticmethod
    async def list_diaries(user_id: int, oldest_first: bool = False):
        query = Diary.filter(user_id=user_id)
        if oldest_first:
            query = query.order_by("created_at")
        else:
            query = query.order_by("-created_at")
        return await query

    @staticmethod
    async def update_diary(diary, title: str = None, content: str = None):
        if title:
            diary.title = title
        if content:
            diary.content = content
        await diary.save()
        return diary

    @staticmethod
    async def delete_diary(diary):
        await diary.delete()
