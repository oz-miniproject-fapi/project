import os
import json
import httpx
from google.oauth2 import service_account
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/cloud-platform"]

class AIService:
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    @staticmethod
    def get_access_token() -> str:
        """서비스 계정 JSON으로 OAuth2 Access Token 발급"""
        service_account_file = os.getenv("GEMINI_API_KEY_PATH")  # 함수 안에서 읽음
        if not service_account_file or not os.path.exists(service_account_file):
            raise ValueError("서비스 계정 JSON 경로가 잘못되었거나 설정되지 않았습니다.")
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        credentials.refresh(Request())
        return credentials.token

    @staticmethod
    async def get_emotion_summary(diary_content: str) -> str:
        token = AIService.get_access_token()
        prompt = f"""
아래는 사용자가 작성한 일기 내용입니다. 이 일기의 핵심 내용을 간결하고 명확하게 요약해 주세요.

---
{diary_content}
---

요약은 2~3문장 이내로 작성해 주세요.
        """
        payload = {
            "prompt": {"text": prompt},
            "temperature": 0.5,
            "max_output_tokens": 200
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AIService.GEMINI_API_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data.get("candidates", [{}])[0].get("content", "")

    @staticmethod
    async def get_emotion_keywords(diary_id: int, user_id: int, diary_content: str) -> list[dict]:
        token = AIService.get_access_token()
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
        payload = {
            "prompt": {"text": prompt},
            "temperature": 0,
            "max_output_tokens": 300
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AIService.GEMINI_API_URL,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            try:
                return json.loads(data.get("candidates", [{}])[0].get("content", "")).get("keywords", [])
            except Exception:
                return []
