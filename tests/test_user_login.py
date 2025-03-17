import pytest
import requests
import allure
from tests.conftest import BASE_URL, unique_user

@allure.feature("User Login")
class TestUserLogin:
    @allure.story("Login with valid credentials")
    def test_login_valid_user(self, unique_user):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": unique_user["email"],
            "password": unique_user["password"]
        })
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.story("Login with invalid credentials")
    @pytest.mark.parametrize("email, password", [
        ("wrong@mail.com", "wrongpassword"),
        ("", "password123"),
        ("test@mail.com", "")
    ])
    def test_login_invalid_credentials(self, email, password):
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"