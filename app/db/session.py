from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def create_engine(db_url: Optional[str] = None) -> AsyncEngine:
    return create_async_engine(db_url or settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


async_engine = create_engine()
AsyncSessionLocal = sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
)
