import logging
import pathlib

from logging import Handler, Logger, StreamHandler
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.handlers import init_error_handles


def setup_logger(
    name: str,
    level: int = logging.INFO,
    debug: bool = False,
    path: str = "./logs/app.log",
    max_bytes: int = 25 * 1024 * 1024,
    backup_count: int = 5,
) -> Logger:
    if debug:
        level = logging.DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(level)

    DEFAULT_FORMAT = (
        "%(asctime)s.%(msecs)03d [%(threadName)s] %(levelname)s %(pathname)s(%(funcName)s:%(lineno)d) - %(message)s"
    )
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(DEFAULT_FORMAT, datefmt=DATE_FORMAT)
    pathlib.Path(path).absolute().parent.mkdir(parents=True, exist_ok=True)
    handlers: list[Handler] = [
        StreamHandler(),
        RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count),
    ]
    for handler in handlers:
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def create_app() -> FastAPI:
    setup_logger("app")
    app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

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
