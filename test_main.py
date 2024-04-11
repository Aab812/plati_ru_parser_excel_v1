import os
import datetime
import json
import requests
import logging

# Создание папки для хранения логов
def create_logs_folder():
    logs_folder = "logs"
    os.makedirs(logs_folder, exist_ok=True)

# Создание папки для хранения логов за текущий месяц
def create_monthly_logs_folder():
    current_month = datetime.datetime.now().strftime("%B").lower()
    logs_month_folder = os.path.join("logs", f"logs_{current_month}")
    os.makedirs(logs_month_folder, exist_ok=True)
    return logs_month_folder

# Получение временной метки
def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

# Логирование запроса
def log_request(url, headers, logs_folder):
    with open(os.path.join(logs_folder, f"logs_{get_timestamp()}.txt"), "a") as file:
        file.write("== Request ==\n")
        file.write(f"URL: {url}\n")
        file.write(f"Headers: {headers}\n\n")

# Логирование ответа
def log_response(response, logs_folder):
    with open(os.path.join(logs_folder, f"logs_{get_timestamp()}.txt"), "a") as file:
        file.write("== Response ==\n")
        file.write(f"URL: {response.url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write("--- Body ---\n")
        response_data = response.json()
        json.dump(response_data, file, indent=4)
        file.write("\n\n")

# Тестовая функция для поиска информации о Spider-Man 2
def test_search_spiderman2():
    url = "https://plati.io/api/search.ashx?query=spider-man-2&visibleOnly=true&response=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    create_logs_folder()  # Создание папки для хранения логов
    logs_folder = create_monthly_logs_folder()  # Создание папки для хранения логов за текущий месяц

    log_request(url, headers, logs_folder)  # Логирование запроса

    try:
        response = requests.get(url, headers=headers)  # Отправка GET-запроса к API
        response.raise_for_status()  # Проверка успешности ответа
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
    else:
        log_response(response, logs_folder)  # Логирование ответа

        # Проверка, что ответ в формате JSON
        content_type = response.headers['Content-Type']
        if "application/json" in content_type or 'text/json' in content_type:
            response_data = response.json()
            keys = {key for item in response_data.get('items', []) for key in item}
            used_keys_order = ["id", "name", "price_rur", "url", "description", "seller_id", "seller_name",
                               "seller_rating", "count_positiveresponses", "count_negativeresponses", "count_returns"]
            print("\nИспользуемые ключи:")
            for key in used_keys_order:
                if key in keys:
                    print(key)

        # Выводим статус код в терминал
        print("Статус код:", response.status_code)

        # Выводим URL в терминал
        print("URL:", url)

if __name__ == '__main__':
    test_search_spiderman2()
