import os
import logging
import unittest
import requests
from datetime import datetime

# Создание директории logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Получение текущего времени
current_time = datetime.now()

# Параметры логирования
log_file = f"logs/logs_{current_time.strftime('%d_%m_%Y_%H_%M')}.log"
log_format = "%(asctime)s - %(levelname)s - %(message)s"

# Настройка логирования
logging.basicConfig(filename=log_file, level=logging.INFO, format=log_format)

class TestPlatiAPI(unittest.TestCase):
    def test_search_spiderman2(self):
        url = "https://plati.io/api/search.ashx?query=spider-man-2&visibleOnly=true&response=json"

        # Отправляем GET-запрос к API
        response = requests.get(url)

        # Проверяем успешность ответа (статус код 200)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что ответ в формате JSON
        content_type = response.headers['Content-Type']
        self.assertTrue('application/json' in content_type or 'text/json' in content_type)

        # Выводим только уникальные ключи из ответа метода в заданном порядке
        response_data = response.json()
        keys = set()
        for item in response_data['items']:
            keys.update(item.keys())
        used_keys_order = ["id", "name", "price_rur", "url", "description", "seller_id", "seller_name",
                     "seller_rating", "count_positiveresponses", "count_negativeresponses", "count_returns"]
        logging.info(" ")
        logging.info("Используемые ключи:")
        for key in used_keys_order:
            if key in keys:
                logging.info(key)

        # Выводим статус код в лог
        logging.info("Статус код: %d", response.status_code)

        # Выводим URL в лог
        logging.info("URL: %s", url)

if __name__ == '__main__':
    unittest.main()
