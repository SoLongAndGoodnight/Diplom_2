import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("User Registration")
class TestUserRegistration:
    @allure.story("Create a unique user")
    def test_create_unique_user(self, unique_user):
        response = requests.post(f"{BASE_URL}/auth/register", json=unique_user)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.story("Create user with missing field")
    @pytest.mark.parametrize("user_data", [
        {"email": "", "password": "password123", "name": "TestUser"},
        {"email": "test@mail.com", "password": "", "name": "TestUser"},
        {"email": "test@mail.com", "password": "password123", "name": ""}
    ])
    def test_create_user_missing_field(self, user_data):
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"