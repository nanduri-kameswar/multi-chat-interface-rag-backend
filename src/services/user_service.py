import uuid
from datetime import datetime, timezone

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_models import JwtPayload
from src.auth.auth_passlib import create_hashed_password
from src.core.config import settings
from src.core.exceptions.exceptions import ConflictError
from src.models.user_model import User
from src.models.user_session_model import UserSession
from src.repositories.user_repository import UserRepository
from src.repositories.user_session_repository import UserSessionRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.session_repo = UserSessionRepository(db)

    @staticmethod
    def create_jwt_token(payload: JwtPayload) -> str:
        to_encode = {
            "sub": str(payload.get("user_id")),
            "type": str(payload.get("token_type")),
            "email": payload.get("email"),
            "role": payload.get("role"),
        }
        expiry_time = datetime.now(tz=timezone.utc) + settings.JWT_EXPIRES_IN
        to_encode.update({"exp": expiry_time})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        return await self.repo.get_user_by_id(user_id)

    async def register_user(self, name: str, email: str, password: str) -> User:
        hashed_password = create_hashed_password(password)
        user = User(name=name, email=email, password_hash=hashed_password)
        return await self.repo.create_user(user)

    async def authenticate_user(self, email: str, password: str) -> User:
        return await self.repo.authenticate_user(email, password)

    async def update_password(
        self,
        user_id: uuid.UUID,
        current_password: str,
        new_password: str,
    ) -> None:
        if current_password == new_password:
            raise ConflictError("Current password and New password cannot be the same")
        return await self.repo.update_password(user_id, current_password, new_password)

    async def create_session(self, user_id: uuid.UUID, refresh_token: str):
        session = UserSession(
            user_id=user_id,
            refresh_token=refresh_token,
            expires_at=datetime.now() + settings.REFRESH_JWT_EXPIRES_IN,
        )
        await self.session_repo.create_session(session)

    async def get_session(self, token: str) -> UserSession:
        return await self.session_repo.get_session(token)

    async def delete_session(self, session: UserSession):
        await self.session_repo.delete_session(session)
