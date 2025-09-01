from app.repositories.tag_repo import TagRepository

class TagService:
    def __init__(self):
        self.tag_repo = TagRepository()

    async def list_tags(self):
        return await self.tag_repo.list_all()
