import asyncio
from app.models.user import User
from tortoise import Tortoise

async def create_test_user():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models": ["app.models.user", "app.models.diary"]}
    )
    await Tortoise.generate_schemas()

    user = await User.get_or_none(id=3)
    if not user:
        await User.create(id=3, email="test@example.com", password="test123")
        print("✅ Test user created")
    else:
        print("✅ Test user already exists")

    await Tortoise.close_connections()

asyncio.run(create_test_user())
