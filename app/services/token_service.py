from app.repositories.token_repo import TokenRepository

class TokenService:
    def __init__(self):
        self.token_repo = TokenRepository()

    async def blacklist_token(self, token: str):
        await self.token_repo.add(token)
        return {"message": "로그아웃 완료"}
