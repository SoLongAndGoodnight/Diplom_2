import pytest
import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture
def unique_user():
    user_data = {
        "email": "unique_user_test@mail.com",
        "password": "password123",
        "name": "UniqueTestUser"
    }
    # Регистрируем пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 403:
        # Если пользователь уже существует — логинимся
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200, "Failed to login existing user"
        token = login_response.json()["accessToken"]
    else:
        # Берем токен сразу после регистрации
        assert response.status_code == 200, f"Failed to register user: {response.status_code}, response: {response.json()}"
        token = response.json()["accessToken"]

    # Передаем данные пользователя и токен в тест
    user_data["token"] = token
    yield user_data

    # Удаляем пользователя после теста
    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
def login(unique_user):
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": unique_user["email"],
        "password": unique_user["password"]
    })
    assert response.status_code == 200, f"Failed to login: {response.status_code}, response: {response.json()}"
    token = response.json().get("accessToken")
    assert token, "Login failed — no token received"
    # Убираем лишнее "Bearer", если оно уже есть
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")
    return token

