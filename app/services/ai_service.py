from app.core.openai_client import analyze_emotion

class AIService:

    @staticmethod
    async def get_emotion_summary(diary_content: str):
        return await analyze_emotion(diary_content)
