from app.models.diary import Diary
from app.models.emotion_keyword import EmotionKeyword
from app.repositories.diary_repo import DiaryRepository
from app.repositories.tag_repo import TagRepository
from app.services.ai_service import AIService

class DiaryService:
    tag_repo = TagRepository()

    @staticmethod
    async def create_diary_with_tags(user_id: int, title: str, content: str, tag_names: list[str]):
        diary = await DiaryRepository.create_diary(user_id, title, content)
        if tag_names:
            tags = [await DiaryService.tag_repo.get_or_create(name) for name in tag_names]
            await diary.tags.add(*tags)
        await DiaryService.analyze_emotion(diary)
        return diary

    @staticmethod
    async def update_diary_with_tags(diary, title: str = None, content: str = None, tag_names: list[str] = None):
        await DiaryRepository.update_diary(diary, title, content)
        if tag_names is not None:
            await diary.tags.clear()
            tags = [await DiaryService.tag_repo.get_or_create(name) for name in tag_names]
            await diary.tags.add(*tags)
        await DiaryService.analyze_emotion(diary)
        return diary

    @staticmethod
    async def get_diary(user_id: int, diary_id: int):
        diary = await DiaryRepository.get_diary_by_id(user_id, diary_id)
        await diary.fetch_related("tags", "emotion_keywords")
        return diary

    @staticmethod
    async def list_diaries(user_id: int, oldest_first: bool = False):
        diaries = await DiaryRepository.list_diaries(user_id, oldest_first)
        for diary in diaries:
            await diary.fetch_related("tags", "emotion_keywords")
        return diaries

    @staticmethod
    async def list_diaries_by_tag(user_id: int, tag_name: str):
        diaries = await DiaryRepository.list_diaries(user_id)
        for diary in diaries:
            await diary.fetch_related("tags", "emotion_keywords")
        return [d for d in diaries if any(tag.name == tag_name for tag in d.tags)]

    @staticmethod
    async def summarize_diary(diary_id: int, user_id: int):
        diary = await DiaryService.get_diary(user_id, diary_id)
        if not diary:
            return None
        summary = await AIService.get_emotion_summary(diary.content)
        return summary

    @staticmethod
    async def analyze_emotion(diary: Diary):
        """일기 내용으로 감정 분석 후 저장"""
        keywords = await AIService.get_emotion_keywords(diary.id, diary.user_id, diary.content)
        if not keywords:
            return []

        # 대표 감정 선택
        emotion_counts = {"긍정": 0, "부정": 0, "중립": 0}
        for kw in keywords:
            emotion_counts[kw["emotion"]] += 1

        if emotion_counts["부정"] > 0:
            diary.emotion = "부정"
        elif emotion_counts["긍정"] > 0:
            diary.emotion = "긍정"
        else:
            diary.emotion = "중립"

        await diary.save()

        # EmotionKeyword 저장
        await EmotionKeyword.filter(diary=diary).delete()  # 기존 키워드 삭제
        for kw in keywords:
            await EmotionKeyword.create(diary=diary, word=kw["word"], emotion=kw["emotion"])

        return keywords

    @staticmethod
    async def analyze_diary_emotions(diary_id: int, user_id: int):
        diary = await DiaryService.get_diary(user_id, diary_id)
        if not diary:
            return None
        keywords = await DiaryService.analyze_emotion(diary)
        return keywords
