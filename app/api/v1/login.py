import logging

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.commons.response import LoginException
from app.core import security
from app.core.config import settings


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_async_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise LoginException("Incorrect email or password")
    elif not crud.user.is_active(user):
        raise LoginException("Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/reset-password", response_model=schemas.Msg)
async def reset_password(
    new_password: str = Body(..., embed=True),
    db: AsyncSession = Depends(deps.get_async_db),
    user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Reset password
    """
    hashed_password = security.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    await db.commit()
    logger.info(f"{user.email} password reset successfully.")
    return schemas.Msg(msg="Password updated successfully")
