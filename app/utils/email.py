# app/utils/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your_email@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your_email_password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "your_email@gmail.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=True,    # TLS 사용
    MAIL_SSL_TLS=False,     # SSL/TLS 사용 여부
    USE_CREDENTIALS=True
)

async def send_verification_email(email: EmailStr, token: str):
    link = f"http://localhost:8000/auth/verify-email?token={token}"
    message = MessageSchema(
        subject="회원가입 이메일 인증",
        recipients=[email],
        body=f"회원가입을 완료하려면 아래 링크를 클릭하세요:\n{link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
