from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.handlers import init_error_handles
from app.tasks.client import arq_client
from app.utils import setup_logger


def create_app() -> FastAPI:
    setup_logger("app")
    app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

    @app.on_event('startup')
    async def starup_event() -> None:
        await arq_client.create_pool(settings.ARQ_REDIS_DSN, settings.ARQ_QUEUE_NAME)

    @app.on_event('shutdown')
    async def shutdown_event() -> None:
        await arq_client.close_pool()

    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    init_error_handles(app)
    return app


app = create_app()
