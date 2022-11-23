from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.commons.response import DuplicatedError, NotFoundException, NotPermittedError


router = APIRouter(prefix="/users")


@router.post("", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    user_in: schemas.UserCreate,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise DuplicatedError("The user with this username already exists in the system.")
    user = await crud.user.create(db, obj_in=user_in)
    return user


@router.get("", response_model=schemas.UserPagingResult)
async def read_users(
    db: AsyncSession = Depends(deps.get_async_db),
    paging: schemas.PagingParams = Depends(deps.get_paging_params),
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    total, users = await crud.user.get_multi(db, skip=paging.skip, limit=paging.limit)
    return paging.populate_result(total, list(users))


@router.get("/me", response_model=schemas.User)
async def read_user_me(current_user: models.User = Depends(deps.get_current_active_user)) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    password: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = await crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_async_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise NotPermittedError("The user doesn't have enough privileges")
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_async_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    _: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = await crud.user.get(db, id=user_id)
    if not user:
        raise NotFoundException(
            "The user with this username does not exist in the system",
        )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
