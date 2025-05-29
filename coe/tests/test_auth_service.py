import pytest
from jose import jwt
from starlette.requests import Request as StarletteRequest
from starlette.datastructures import Headers
from starlette.testclient import TestClient
from fastapi import HTTPException, Request
from coe.services import auth_service
from coe.schemas.user import CreateUser
from coe.services.user_service import create_user
from config import settings
from faker import Faker

faker = Faker()
SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm

def create_test_user(db):
    data = CreateUser(
        first_name=faker.first_name(),
        last_name=faker.last_name(),
        email=faker.email(),
        password="testpass"
    )
    user = create_user(data, db)
    return user

def test_create_access_token_contains_user_id():
    data = {"user_id": 1}
    token = auth_service.create_access_token(data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["user_id"] == 1
    assert "exp" in payload

def test_create_refresh_token_has_type_refresh():
    data = {"user_id": 1}
    token = auth_service.create_refresh_token(data)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["user_id"] == 1
    assert payload["type"] == "refresh"
    assert "exp" in payload

def test_get_current_user(db):
    # Create a test user
    user = create_test_user(db)
    token = auth_service.create_access_token({"user_id": user.id})

    # Build a fake scope with proper cookie header
    cookie_header = f"access_token={token}"
    headers = Headers({
        "cookie": cookie_header
    })

    scope = {
        "type": "http",
        "headers": headers.raw,
    }
    request = StarletteRequest(scope)

    # Call get_current_user with the mocked request
    current_user = auth_service.get_current_user(request=request, db=db)

    # Assertions
    assert current_user.id == user.id
    assert current_user.email == user.email

def test_get_current_user_invalid_token(db):
    with pytest.raises(HTTPException) as exc:
        scope = {
            "type": "http",
            "headers": Headers({}).raw,
            "cookies": {"access_token": 'token-invalid'}
        }
        request = StarletteRequest(scope)

        auth_service.get_current_user(request=request, db=db)
    assert exc.value.status_code == 401
