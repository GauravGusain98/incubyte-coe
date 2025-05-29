from faker import Faker
from fastapi.testclient import TestClient

faker = Faker()


def register_user(client: TestClient, password: str = "secret123"):
    user_data = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.unique.email(),
        "password": password
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 201, "User registration failed"
    return response.json()["userId"], user_data["email"], user_data["password"]


def login_user(client: TestClient, email: str, password: str):
    response = client.post("/user/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200, "Login failed"
    return response.json()["accessToken"], response.json().get("refreshToken")


def test_register_user(client: TestClient):
    user_data = {
        "firstName": faker.first_name(),
        "lastName": faker.last_name(),
        "email": faker.unique.email(),
        "password": "secret123"
    }
    response = client.post("/user/register", json=user_data)
    assert response.status_code == 201
    assert "userId" in response.json()


def test_login_user(client: TestClient):
    _, email, password = register_user(client)
    response = client.post("/user/login", json={"email": email, "password": password})
    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_update_user_route(client: TestClient):
    user_id, email, password = register_user(client, "update123")
    access_token, _ = login_user(client, email, "update123")

    update_data = {"firstName": faker.first_name()}
    response = client.put(
        f"/user/{user_id}",
        json=update_data,
        cookies={"access_token": access_token}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User data updated successfully"


def test_delete_user_route(client: TestClient):
    user_id, email, password = register_user(client, "toDelete123")
    access_token, _ = login_user(client, email, "toDelete123")

    response = client.delete(
        f"/user/{user_id}",
        cookies={"access_token": access_token}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "User removed successfully"


def test_refresh_token(client: TestClient):
    _, email, password = register_user(client, "refresh123")
    _, refresh_token = login_user(client, email, "refresh123")

    response = client.post(
        "/user/token/refresh",
        cookies={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    assert "accessToken" in response.json()
