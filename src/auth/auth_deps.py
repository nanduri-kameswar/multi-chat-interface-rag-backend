from typing import Annotated, TypeAlias

from fastapi import Cookie, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from src.core.config import settings
from src.core.exceptions.exceptions import CredentialsError
from src.db.connection import engine

from .auth_models import JwtPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")
OAuth2Bearer_Dependency: TypeAlias = Annotated[str, Depends(oauth2_scheme)]
OAuth2Form_Dependency: TypeAlias = Annotated[OAuth2PasswordRequestForm, Depends()]

JWT_Cookie: TypeAlias = Annotated[str | None, Cookie()]

""" Use JWT_Cookie for more safety otherwise Use OAuth2Bearer_Dependency"""


def get_current_user(access_token: JWT_Cookie = None) -> JwtPayload:
    if not access_token:
        raise CredentialsError("Not authenticated")
    try:
        payload = jwt.decode(
            access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = (
            str(payload.get("sub"))
            if engine.dialect.name == "postgresql"
            else payload["sub"]
        )
        token_type = payload.get("token_type")
        email = payload.get("email")
        role = payload.get("role")
        if not user_id or not email or not role:
            raise CredentialsError("Invalid token")
        return JwtPayload(
            user_id=str(user_id), token_type=token_type, email=email, role=role
        )
    except JWTError:
        raise CredentialsError("Invalid or expired token")


CurrentUser_Dependency: TypeAlias = Annotated[JwtPayload, Depends(get_current_user)]
