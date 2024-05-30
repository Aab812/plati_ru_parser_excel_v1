import requests
import allure
import pytest
from api_plati_ru_parser import api_platti_ru_from_developers
@allure.title("Тест на api plati_ru")
def test_api_plati_ru_parser():
    response =api_platti_ru_from_developers()
    with allure.step(f'Проверить статус-код: ожидаем 200, получаем {response.status_code}'):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


if __name__ == "__main__":
    test_api_plati_ru_parser()