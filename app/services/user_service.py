from app.models.user import User
from app.schemas.user import UserProfileResponse, UserUpdateRequest, UserDeleteResponse
from tortoise.exceptions import DoesNotExist, IntegrityError

class UserService:

    # --- 내 프로필 조회 ---
    async def get_profile(self, user: User) -> UserProfileResponse:
        return UserProfileResponse(
            id=user.id,
            email=user.email,
            nickname=user.nickname,
            name=user.name,
            phone=user.phone,
            created_at=user.created_at
        )

    # --- 내 정보 수정 ---
    async def update_user(self, user: User, data: dict) -> UserProfileResponse:
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

    # --- 내 계정 삭제 ---
    async def delete_user(self, user: User) -> UserDeleteResponse:
        try:
            await user.delete()
            return UserDeleteResponse(status="success", message="User deleted")
        except IntegrityError:
            raise ValueError("Cannot delete user: related data exists")
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            raise
