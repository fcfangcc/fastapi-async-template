from typing import Dict, Generator, AsyncGenerator
import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from app.core.config import settings
from app.db.session import create_engine
from app.main import create_app
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope='session')
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def engine() -> Generator:
    engine = create_engine()
    yield engine
    engine.sync_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db(engine: AsyncEngine) -> AsyncGenerator:
    async with AsyncSession(engine) as session:
        yield session
    await session.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(create_app()) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest_asyncio.fixture(scope="module")
async def normal_user_token_headers(client: TestClient, db: AsyncSession) -> Dict[str, str]:
    return await authentication_token_from_email(client=client, email=settings.EMAIL_TEST_USER, db=db)
