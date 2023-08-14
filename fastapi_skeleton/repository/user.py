from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_skeleton.common.util.repository import Repository
from fastapi_skeleton.schema.user import User


class UserRepository(Repository[User]):
    async def find_by_user_id(self, session: AsyncSession, user_id: str):
        result = await session.execute(select(User).where(User.user_id == user_id))
        return result.scalars().one_or_none()
