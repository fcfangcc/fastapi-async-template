from fastapi import APIRouter

from . import users
from . import login

api_router = APIRouter()
api_router.include_router(users.router, tags=["user"])
api_router.include_router(login.router, tags=["login"])
