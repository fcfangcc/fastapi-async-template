from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def create_engine(db_url: Optional[str] = None, execution_options: Optional[dict[str, str]] = None) -> AsyncEngine:
    return create_async_engine(
        db_url or settings.SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        execution_options=execution_options,
    )


_ASYNC_ENGINE: AsyncEngine = None  # type: ignore[assignment]
_ASYNC_SESSION_LOCAL: sessionmaker = None  # type: ignore[assignment]


def set_async_engine(engine: AsyncEngine) -> None:
    """for test"""
    global _ASYNC_ENGINE
    global _ASYNC_SESSION_LOCAL
    _ASYNC_ENGINE = engine
    _ASYNC_SESSION_LOCAL = sessionmaker(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
    )


def get_async_engine() -> AsyncEngine:
    return _ASYNC_ENGINE


def get_session_local() -> sessionmaker:
    return _ASYNC_SESSION_LOCAL


set_async_engine(create_engine())
