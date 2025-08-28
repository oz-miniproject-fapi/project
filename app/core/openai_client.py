import os
import openai
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 가져오기

openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_emotion(text: str) -> str:
    """
    입력된 텍스트를 AI로 감정 분석 후 요약
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 감정 분석 전문가입니다."},
            {"role": "user", "content": f"다음 문장의 감정을 요약해줘: {text}"}
        ],
        temperature=0.5,
    )
    summary = response.choices[0].message.content
    return summary
