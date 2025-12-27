import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class MessageRole(str, enum.Enum):
    SYSTEM = "system"
    ASSISTANT = "assistant"
    USER = "user"
