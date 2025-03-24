## Дипломный проект. Задание 2: API-тесты

### Структура проекта
tests - тесты

Запуск тестов и генерация отчета:

pytest --alluredir=allure-results

Генерация и просмотр отчета:

allure serve allure-results

Проверка покрытия:
pytest --cov=tests

Установка зависимостей:

pip install -r requirements.txt
