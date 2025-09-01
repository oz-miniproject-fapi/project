from app.models.user import User
from app.schemas.user import UserProfileResponse, UserUpdateRequest, UserDeleteResponse
from tortoise.exceptions import DoesNotExist

class UserService:
    def __init__(self, db):
        self.db = db

    # --- 내 프로필 조회 ---
    async def get_profile(self, user_id: int) -> UserProfileResponse:
        try:
            user = await User.get(id=user_id)
            return UserProfileResponse(
                id=user.id,
                email=user.email,
                nickname=user.nickname,
                name=user.name,
                phone=user.phone,
                created_at=user.created_at
            )
        except DoesNotExist:
            raise ValueError("User not found")

    # --- 내 정보 수정 ---
    async def update_user(self, user_id: int, data: dict) -> UserProfileResponse:
        try:
            user = await User.get(id=user_id)
            for key, value in data.items():
                setattr(user, key, value)
            await user.save()
            return UserProfileResponse(
                id=user.id,
                email=user.email,
                nickname=user.nickname,
                name=user.name,
                phone=user.phone,
                created_at=user.created_at
            )
        except DoesNotExist:
            raise ValueError("User not found")

    # --- 내 계정 삭제 ---
    async def delete_user(self, user_id: int) -> UserDeleteResponse:
        try:
            user = await User.get(id=user_id)
            await user.delete()
            return UserDeleteResponse()
        except DoesNotExist:
            raise ValueError("User not found")
