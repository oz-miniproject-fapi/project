from app.models.diary import Diary
from app.models.user import User

class DiaryRepository:
    @staticmethod
    async def create_diary(user_id: int, title: str, content: str):
        # User 객체 조회 후 ForeignKey 전달
        user = await User.get(id=user_id)
        return await Diary.create(user=user, title=title, content=content)

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

    # 🔎 1. 키워드 검색
    @staticmethod
    async def search_diaries(user_id: int, keyword: str):
        return await Diary.filter(
            user_id=user_id,
            content__icontains=keyword
        ).all()

    # 🏷 2. 태그 기반 조회 (10개 제한)
    @staticmethod
    async def list_diaries_by_tag(user_id: int, tag_name: str, limit: int = 10):
        return (
            await Diary.filter(user_id=user_id, tags__name=tag_name)
            .prefetch_related("tags", "emotion_keywords")
            .limit(limit)
        )
