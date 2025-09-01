from app.models.tag import Tag

class TagRepository:
    async def get_or_create(self, name: str):
        tag, _ = await Tag.get_or_create(name=name)
        return tag

    async def list_all(self):
        return await Tag.all()
