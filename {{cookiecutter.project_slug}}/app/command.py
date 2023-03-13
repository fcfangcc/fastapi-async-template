from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user
from app.schemas import UserCreate


async def insert_default_data(session: AsyncSession) -> None:
    if not await user.get_by_email(session, email=settings.FIRST_SUPERUSER):
        obj = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            nick_name=settings.FIRST_SUPERUSER,
        )
        obj.is_superuser = True
        await user.create(session, obj_in=obj)
        print(f"{settings.FIRST_SUPERUSER} create successfully.")
    else:
        print(f"{settings.FIRST_SUPERUSER} user is exist.")
