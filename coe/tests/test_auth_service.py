import pytest
from jose import jwt
from fastapi import HTTPException
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

def test_verify_token_valid():
    data = {"user_id": 123}
    token = auth_service.create_access_token(data)
    result = auth_service.verify_token(token, credentials_exception=HTTPException(status_code=401))
    assert result == 123

def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc:
        auth_service.verify_token("invalid.token.value", credentials_exception=HTTPException(status_code=401))
    assert exc.value.status_code == 401

def test_get_current_user(db):
    user = create_test_user(db)
    token = auth_service.create_access_token({"user_id": user.id})

    result = auth_service.get_current_user(token=token, db=db)
    assert result.id == user.id
    assert result.email == user.email

def test_get_current_user_invalid_token(db):
    with pytest.raises(HTTPException) as exc:
        auth_service.get_current_user(token="invalid.token.here", db=db)
    assert exc.value.status_code == 401
