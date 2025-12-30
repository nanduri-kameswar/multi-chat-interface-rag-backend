from uuid import UUID

from fastapi import APIRouter, Request, Response

from src.auth.auth_deps import CurrentUser_Dependency, OAuth2Form_Dependency
from src.auth.auth_models import JwtPayload
from src.core.exceptions.exceptions import (
    CredentialsError,
    ForbiddenError,
    NotFoundError,
)
from src.models.user_model import User
from src.models.user_session_model import UserSession as UserSession
from src.schemas.user_schema import UserCreate, UserResponse, UserUpdate

from .routers_deps import UserService_Dependency

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, service: UserService_Dependency):
    return await service.register_user(user.name, str(user.email), user.password)


@router.post("/login")
async def login_user(
    response: Response,
    form_data: OAuth2Form_Dependency,
    user_service: UserService_Dependency,
    session_service: UserService_Dependency,
):
    user: User = await user_service.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise ForbiddenError("Invalid credentials")
    access_payload = JwtPayload(
        user_id=str(user.id),
        token_type="access",
        email=str(user.email),
        role=str(user.role),
    )
    refresh_payload = JwtPayload(
        user_id=str(user.id),
        token_type="refresh",
        email=str(user.email),
        role=str(user.role),
    )
    access_token: str = user_service.create_jwt_token(access_payload)
    refresh_token: str = user_service.create_jwt_token(refresh_payload)

    await session_service.create_session(user.id, refresh_token)

    response.set_cookie(
        "access_token", access_token, httponly=True, secure=True, samesite="lax"
    )

    response.set_cookie(
        "refresh_token", refresh_token, httponly=True, secure=True, samesite="lax"
    )

    return {"message": "Login successful"}


@router.post("/logout")
async def logout(
    request: Request, response: Response, session_service: UserService_Dependency
):
    token = request.cookies.get("refresh_token")
    if token:
        try:
            session: UserSession = await session_service.get_session(token)
            await session_service.delete_session(session)
        except NotFoundError:
            pass

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}


@router.post("/refresh")
async def refresh(
    request: Request,
    response: Response,
    user_service: UserService_Dependency,
    session_service: UserService_Dependency,
):
    token = request.cookies.get("refresh_token")
    if not token:
        raise CredentialsError("Refresh token not found")

    session = await session_service.get_session(token)
    user = await user_service.get_user_by_id(session.user_id)

    access_payload = JwtPayload(
        user_id=str(user.id),
        token_type="access",
        email=str(user.email),
        role=str(user.role),
    )
    refresh_payload = JwtPayload(
        user_id=str(user.id),
        token_type="refresh",
        email=str(user.email),
        role=str(user.role),
    )
    new_access_token: str = user_service.create_jwt_token(access_payload)
    new_refresh_token: str = user_service.create_jwt_token(refresh_payload)

    await session_service.delete_session(session)

    await session_service.create_session(user.id, new_refresh_token)

    response.set_cookie(
        "access_token",
        new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {"status": "refreshed"}


@router.get("/me", response_model=UserResponse)
async def get_me(jwt: CurrentUser_Dependency, service: UserService_Dependency):
    user: User = await service.get_user_by_id(UUID(jwt.get("user_id")))
    return user


@router.put("/update-password")
async def update_password(
    payload: UserUpdate, jwt: CurrentUser_Dependency, service: UserService_Dependency
):
    return await service.update_password(
        UUID(jwt.get("user_id")),
        payload.current_password,
        payload.new_password,
    )
