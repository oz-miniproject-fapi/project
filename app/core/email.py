from fastapi import BackgroundTasks

# 실제 프로젝트에서는 SMTP 서버 설정 필요
def send_verification_email(email: str, token: str):
    # 예시: 이메일 보내기
    print(f"[EMAIL] To: {email}, Verification token: {token}")

def send_verification_email_background(email: str, token: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_verification_email, email, token)
