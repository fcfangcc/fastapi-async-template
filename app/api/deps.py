from typing import Generator, AsyncGenerator, AsyncContextManager, Callable
from contextlib import asynccontextmanager

from fastapi import Depends, Query
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal, AsyncSessionLocal
from app.commons.response import LoginException, NotPermittedError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_paging_params(page: int = Query(1, ge=1), per_page: int = Query(20, ge=1)) -> schemas.PagingParams:
    return schemas.PagingParams(page=page, per_page=per_page)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db = AsyncSessionLocal()
        yield db
    finally:
        await db.close()


async_db_context: Callable[[], AsyncContextManager[AsyncSession]] = asynccontextmanager(get_async_db)


async def get_current_user(
    db: AsyncSession = Depends(get_async_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise LoginException("Could not validate credentials")
    user = await crud.user.get(db, id=token_data.sub)
    if not user:
        raise LoginException("User not found")
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user), ) -> models.User:
    if not crud.user.is_active(current_user):
        raise LoginException("Inactive user")
    return current_user


def get_current_active_superuser(current_user: models.User = Depends(get_current_user), ) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise NotPermittedError("The user doesn't have enough privileges")
    return current_user
