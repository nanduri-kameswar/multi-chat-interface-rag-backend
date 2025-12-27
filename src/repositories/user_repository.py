import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_passlib import create_hashed_password, verify_hashed_password
from src.core.exceptions.exceptions import (
    ConflictError,
    CredentialsError,
    NotFoundError,
)
from src.models.user_model import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_user_by_email(self, email: str) -> User:
        result = await self.db.execute(select(User).filter(User.email == email))
        user: User | None = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user: User | None = await self.db.get(User, user_id)
        if not user:
            raise NotFoundError("User does not exist.")
        return user

    async def create_user(self, user: User) -> User:
        if await self._get_user_by_email(str(user.email)):
            raise ConflictError(f"User with {user.email} already exists.")
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def authenticate_user(self, email: str, password: str) -> User:
        result = await self.db.execute((select(User).filter(User.email == email)))
        user: User | None = result.scalar_one_or_none()
        if user and verify_hashed_password(password, str(user.password_hash)):
            return user
        raise CredentialsError("Incorrect email or password")

    async def update_password(
        self,
        user_id: uuid.UUID,
        current_password: str,
        new_password: str,
    ) -> None:
        result = await self.db.execute(select(User).filter(User.id == user_id))
        db_user: User | None = result.scalar_one_or_none()
        if (
            db_user
            and user_id == db_user.id
            and verify_hashed_password(current_password, str(db_user.password_hash))
        ):
            db_user.password_hash = create_hashed_password(new_password)
            await self.db.commit()
        else:
            raise CredentialsError("Current password is not correct.")
