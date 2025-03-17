import requests
import allure
from tests.conftest import BASE_URL, login

@allure.feature("User Orders")
class TestUserOrders:
    @allure.story("Get orders with authorization")
    def test_get_orders_with_auth(self, login):
        headers = {"Authorization": f"Bearer {login}"}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.story("Get orders without authorization")
    def test_get_orders_no_auth(self):
        response = requests.get(f"{BASE_URL}/orders")
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"