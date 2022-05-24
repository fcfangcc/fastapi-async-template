import pytest

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_users_superuser_me(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


@pytest.mark.asyncio
async def test_get_users_normal_user_me(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


@pytest.mark.asyncio
async def test_update_me(client: TestClient, normal_user_token_headers: dict) -> None:
    email = random_email()
    data = {"email": email, "password": random_lower_string()}
    r = client.put(f"{settings.API_V1_STR}/users/me", json=data, headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["email"] == email


@pytest.mark.asyncio
async def test_get_user(
    client: TestClient,
    superuser_token_headers: dict,
    normal_user_token_headers: dict[str, str],
    db: AsyncSession,
) -> None:
    user, _ = await create_random_user(db)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    api_user = r.json()
    existing_user = await crud.user.get_by_email(db, email=user.email)
    assert existing_user
    assert existing_user.email == api_user["email"]
    # NOT_PERMITTED. get another user info
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 400
    assert "NOT_PERMITTED" in r.text


@pytest.mark.asyncio
async def test_update_user(client: TestClient, superuser_token_headers: dict, db: AsyncSession) -> None:
    user, _ = await create_random_user(db)
    user_id = user.id
    data = {"email": random_email(), "password": random_lower_string()}
    r = client.put(
        f"{settings.API_V1_STR}/users/{user.id}",
        json=data,
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    api_user = r.json()
    db.expire(user)  # 不然取到缓存的结果
    existing_user = await crud.user.get(db, id=user_id)
    assert existing_user
    assert existing_user.email == api_user["email"]
    # user not existing
    r = client.put(
        f"{settings.API_V1_STR}/users/0",
        json=data,
        headers=superuser_token_headers,
    )
    assert r.status_code == 400
    assert "NOT_FOUND" in r.text


@pytest.mark.asyncio
async def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: AsyncSession
) -> None:
    user, password = await create_random_user(db)
    data = {"email": user.email, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_create_user(client: TestClient, superuser_token_headers: dict, db: AsyncSession) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 200
    assert "email" in created_user


@pytest.mark.asyncio
async def test_create_user_by_normal_user(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_retrieve_users(client: TestClient, superuser_token_headers: dict, db: AsyncSession) -> None:
    await create_random_user(db)
    await create_random_user(db)
    r = client.get(f"{settings.API_V1_STR}/users", headers=superuser_token_headers)
    data = r.json()

    assert "items" in data
    assert len(data["items"]) > 1
    for item in data["items"]:
        assert "email" in item
