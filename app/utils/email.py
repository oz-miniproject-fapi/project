# app/utils/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME="your_email@gmail.com",   # 본인 이메일
    MAIL_PASSWORD="your_email_password",    # 앱 비밀번호 추천
    MAIL_FROM="your_email@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
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
