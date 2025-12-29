class NotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message


class ForbiddenError(Exception):
    def __init__(self, message: str):
        self.message = message


class BadRequestError(Exception):
    def __init__(self, message: str):
        self.message = message


class ConflictError(Exception):
    def __init__(self, message: str):
        self.message = message


class CredentialsError(Exception):
    def __init__(self, message: str):
        self.message = message


class ProcessingFailedError(Exception):
    def __init__(self, message: str):
        self.message = message


class UnsupportedFileTypeError(Exception):
    def __init__(self, message: str):
        self.message = message
