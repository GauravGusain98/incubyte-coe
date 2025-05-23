from faker import Faker
from fastapi.testclient import TestClient

faker = Faker()


def register_user(client: TestClient, password: str = "secret123"):
    user_data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.unique.email(),
        "password": password
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 201, "User registration failed"
    return response.json()["user_id"], user_data["email"], user_data["password"]


def login_user(client: TestClient, email: str, password: str):
    response = client.post("/user/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200, "Login failed"
    return response.json()["access_token"], response.json().get("refresh_token")


def test_register_user(client: TestClient):
    user_data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.unique.email(),
        "password": "secret123"
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 201
    assert "user_id" in response.json()


def test_login_user(client: TestClient):
    _, email, password = register_user(client)
    response = client.post("/user/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_update_user_route(client: TestClient):
    user_id, email, password = register_user(client, "update123")
    access_token, _ = login_user(client, email, "update123")

    update_data = {"first_name": faker.first_name()}
    response = client.put(
        f"/user/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User data updated successfully"


def test_delete_user_route(client: TestClient):
    user_id, email, password = register_user(client, "toDelete123")
    access_token, _ = login_user(client, email, "toDelete123")

    response = client.delete(
        f"/user/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User removed successfully"


def test_refresh_token(client: TestClient):
    _, email, password = register_user(client, "refresh123")
    _, refresh_token = login_user(client, email, "refresh123")

    response = client.post("/user/token/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    assert "access_token" in response.json()
