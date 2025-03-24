import pytest
import requests
import allure
import time
import random
from tests.conftest import BASE_URL, login


@allure.feature("User Data Modification")
class TestUserModification:
    @allure.title("Modify user data with authorization")
    @pytest.mark.parametrize("field, new_value", [
        ("name", "NewName"),
        ("email", f"newemail{int(time.time())}{random.randint(1000, 9999)}@test.com")
    ])
    def test_modify_user_data_authorized(self, login, field, new_value):
        headers = {"Authorization": f"Bearer {login}"}
        print(f"Headers: {headers}")

        # Модифицируем данные пользователя
        response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json={field: new_value})
        assert response.status_code == 200, f"Expected 200, got {response.status_code}, response: {response.json()}"
        assert response.json()["success"] is True, "User data modification failed"
        assert response.json()["user"][field] == new_value, f"Expected {new_value}, got {response.json()['user'][field]}"


    @allure.title("Modify user data without authorization")
    def test_modify_user_data_unauthorized(self):
        response = requests.patch(f"{BASE_URL}/auth/user", json={"name": "NewName"})
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"