import os
import datetime
import requests

def create_logs_folder():
    logs_folder = "logs"
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

def create_monthly_logs_folder():
    current_month = datetime.datetime.now().strftime("%B").lower()
    logs_month_folder = os.path.join("logs", f"logs_{current_month}")
    if not os.path.exists(logs_month_folder):
        os.makedirs(logs_month_folder)
    return logs_month_folder

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

def log_request(url, headers):
    logs_folder = create_monthly_logs_folder()
    with open(os.path.join(logs_folder, f"logs_{get_timestamp()}.txt"), "a") as file:
        file.write("Request:\n")
        file.write(f"URL: {url}\n")
        file.write(f"Headers: {headers}\n\n")

def log_response(response):
    logs_folder = create_monthly_logs_folder()
    with open(os.path.join(logs_folder, f"logs_{get_timestamp()}.txt"), "a") as file:
        file.write("Response:\n")
        file.write(f"URL: {response.url}\n")
        file.write(f"Status Code: {response.status_code}\n")
        file.write(f"Body: {response.text}\n\n")

def test_search_spiderman2():
    url = "https://plati.io/api/search.ashx?query=spider-man-2&visibleOnly=true&response=json"
    headers = {"User-Agent": "Mozilla/5.0"}

    create_logs_folder()

    log_request(url, headers)

    # Отправляем GET-запрос к API
    response = requests.get(url, headers=headers)

    log_response(response)

    # Проверяем успешность ответа (статус код 200)
    assert response.status_code == 200

    # Проверяем, что ответ в формате JSON
    assert "application/json" in response.headers['Content-Type'] or 'text/json' in response.headers['Content-Type']

    # Выводим только уникальные ключи из ответа метода в заданном порядке
    response_data = response.json()
    keys = set()
    for item in response_data['items']:
        keys.update(item.keys())
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
