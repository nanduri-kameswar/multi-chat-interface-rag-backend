from typing import Literal, TypedDict


class JwtPayload(TypedDict):
    user_id: str
    token_type: Literal["access", "refresh"]
    email: str
    role: str
