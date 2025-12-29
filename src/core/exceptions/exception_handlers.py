from fastapi.responses import JSONResponse

from src.core.exceptions.exceptions import (
    ConflictError,
    CredentialsError,
    ForbiddenError,
    NotFoundError,
    ProcessingFailedError,
    UnsupportedFileTypeError,
)


def register_exception_handlers(app):
    @app.exception_handler(ConflictError)
    def conflict(_, exc: ConflictError):
        return JSONResponse(
            status_code=409,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(NotFoundError)
    def not_found(_, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(ForbiddenError)
    def forbidden(_, exc: ForbiddenError):
        return JSONResponse(
            status_code=403,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(CredentialsError)
    def credentials(_, exc: CredentialsError):
        return JSONResponse(
            status_code=401,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(ProcessingFailedError)
    def credentials(_, exc: ProcessingFailedError):
        return JSONResponse(
            status_code=401,
            content={
                "detail": exc.message,
            },
        )

    @app.exception_handler(UnsupportedFileTypeError)
    def credentials(_, exc: UnsupportedFileTypeError):
        return JSONResponse(
            status_code=401,
            content={
                "detail": exc.message,
            },
        )
