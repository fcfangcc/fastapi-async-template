from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps
from app.commons.response import DuplicatedError, NotFoundException

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
        raise NotFoundException("The user with this username does not exist in the system", )
    user = await crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
