from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


class UserCRUD:
    async def get_user(
            self, email: str, session: AsyncSession) -> Optional[User]:
        user = await session.execute(
            select(User).where(User.email == email))
        return user.scalars().first()


user_crud = UserCRUD()
