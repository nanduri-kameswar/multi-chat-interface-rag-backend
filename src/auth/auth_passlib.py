from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(password: str) -> str:
    return pwd_context.hash(password.encode("utf-8"))


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password.encode("utf-8"), hashed_password)
