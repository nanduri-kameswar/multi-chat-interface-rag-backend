from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.exceptions import NotFoundError
from src.models.user_session_model import UserSession


class UserSessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, session: UserSession):
        self.db.add(session)
        await self.db.commit()

    async def get_session(self, token: str) -> UserSession:
        result = await self.db.execute(
            select(UserSession).filter(UserSession.refresh_token == token)
        )
        session: UserSession | None = result.scalar_one_or_none()
        if not session:
            raise NotFoundError("Invalid refresh token")
        return session

    async def delete_session(self, session: UserSession):
        await self.db.delete(session)
        await self.db.commit()
