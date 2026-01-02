from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.exceptions.exception_handlers import register_exception_handlers
from src.db.connection import init_vector_store
from src.routers import (
    conversation_router,
    document_router,
    llm_router,
    message_router,
    user_router,
)


@asynccontextmanager
async def lifespan(app_name: FastAPI):
    async with init_vector_store() as vector_store:
        app.state.vector_store = vector_store
        yield


app = FastAPI(
    root_path=settings.API_PREFIX,
    lifespan=lifespan,
)

# Added CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers
register_exception_handlers(app)

# Include the routers
app.include_router(user_router.router)
app.include_router(conversation_router.router)
app.include_router(message_router.router)
app.include_router(document_router.router)
app.include_router(llm_router.router)


# home routers
@app.get("/")
def main():
    return {"status": "healthy"}
