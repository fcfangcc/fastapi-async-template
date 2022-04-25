from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import user
from app.schemas import UserCreate


def insert_default_data(session: Session) -> None:
    obj = UserCreate(email=settings.FIRST_SUPERUSER, password=settings.FIRST_SUPERUSER_PASSWORD)
    obj.is_superuser = True
    user.create(session, obj_in=obj)
