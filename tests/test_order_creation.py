import requests
import allure
from tests.conftest import BASE_URL, login


@allure.feature("Order Creation")
class TestOrderCreation:
    @allure.story("Create order with authorization and ingredients")
    def test_create_order_with_auth(self, login):
        # Получаем список ингредиентов
        ingredients_response = requests.get(f"{BASE_URL}/ingredients")
        assert ingredients_response.status_code == 200, f"Failed to fetch ingredients: {ingredients_response.status_code}"

        ingredients_data = ingredients_response.json()
        assert ingredients_data["success"] is True, "Ingredients response didn't return success"

        # Берем первые два ингредиента
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
        assert len(ingredient_ids) == 2, "Not enough ingredients fetched"

        # Формируем заказ
        order_data = {"ingredients": ingredient_ids}

        response = requests.post(f"{BASE_URL}/orders", json=order_data)

        # Проверяем результат
        assert response.status_code == 200, f"Expected 200, got {response.status_code}, response: {response.json()}"
        assert response.json()["success"] is True

    @allure.story("Create order without ingredients")
    def test_create_order_no_ingredients(self, login):
        #headers = {"Authorization": f"Bearer {login}"}
        order_data = {"ingredients": []}
        response = requests.post(f"{BASE_URL}/orders", json=order_data)
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"