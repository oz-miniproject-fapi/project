from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "last_login" TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "is_active" SET DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "last_login";
        ALTER TABLE "user" ALTER COLUMN "is_active" SET DEFAULT False;"""
