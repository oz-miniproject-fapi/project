# app/core/openai_client.py
import os
import httpx

async def analyze_emotion(diary_content: str) -> str:
    """
    Gemini/OpenAI API를 호출해서 일기 내용을 요약하거나 감정을 분석
    """
    GEMINI_API_URL = "https://api.gemini.example/summarize"  # 실제 API URL로 변경
    API_KEY = os.getenv("GEMINI_API_KEY")

    prompt = f"""
    아래는 사용자가 작성한 일기 내용입니다. 이 일기의 핵심 내용을 간결하고 명확하게 요약해 주세요.

    ---
    {diary_content}
    ---

    요약은 2~3문장 이내로 작성해 주세요.
    """

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GEMINI_API_URL,
            json={"prompt": prompt},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("summary", "")
