import os
import json
import httpx
from dotenv import load_dotenv

# .env 로드
load_dotenv()

class AIService:
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    @staticmethod
    async def _post_to_gemini(payload: dict) -> dict:
        if not AIService.GEMINI_API_KEY:
            raise ValueError("Gemini API Key가 설정되지 않았습니다.")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AIService.GEMINI_API_URL,
                headers={
                    "Authorization": f"Bearer {AIService.GEMINI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    async def get_emotion_summary(diary_content: str) -> str:
        prompt = f"""
아래는 사용자가 작성한 일기 내용입니다. 이 일기의 핵심 내용을 간결하고 명확하게 요약해 주세요.

---
{diary_content}
---

요약은 2~3문장 이내로 작성해 주세요.
        """
        payload = {"prompt": {"text": prompt}, "temperature": 0.5, "max_output_tokens": 200}
        data = await AIService._post_to_gemini(payload)
        return data.get("candidates", [{}])[0].get("content", "")

    @staticmethod
    async def get_emotion_keywords(diary_id: int, user_id: int, diary_content: str) -> list[dict]:
        prompt = f"""
아래는 사용자가 작성한 일기 내용입니다. 각 문장에서 나타나는 감정 키워드를 추출해주세요.
긍정, 부정, 중립으로 나누어 JSON 형태로 반환합니다.

{{
  "diary_id": {diary_id},
  "user_id": {user_id},
  "keywords": []
}}

---
{diary_content}
---
        """
        payload = {"prompt": {"text": prompt}, "temperature": 0, "max_output_tokens": 300}
        data = await AIService._post_to_gemini(payload)
        text_output = data.get("candidates", [{}])[0].get("content", "")
        try:
            keywords = json.loads(text_output).get("keywords", [])
        except Exception:
            keywords = []
        return keywords
