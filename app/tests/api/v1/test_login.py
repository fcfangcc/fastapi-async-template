from fastapi.testclient import TestClient
import pytest

from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


@pytest.mark.asyncio
async def test_use_error_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": random_lower_string(),
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    result = r.json()
    assert r.status_code == 400
    assert result["ok"] is False
    assert result["detail"]["code"] == 'LOGIN_ERROR'

    login_data = {
        "username": random_email(),
        "password": random_lower_string(),
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    result = r.json()
    assert r.status_code == 400
    assert result["ok"] is False
    assert result["detail"]["code"] == 'LOGIN_ERROR'


@pytest.mark.asyncio
async def test_use_access_token(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


@pytest.mark.asyncio
async def test_use_reset_password(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    data = {"new_password": random_lower_string()}
    r = client.post(f"{settings.API_V1_STR}/reset-password", headers=normal_user_token_headers, json=data)
    assert r.status_code == 200
