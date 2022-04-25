from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine

from app.core.config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


async_engine = create_engine()
AsyncSessionLocal = sessionmaker(
    bind=async_engine, autocommit=False, autoflush=False, expire_on_commit=False, class_=AsyncSession
)
