import os
import subprocess
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import openpyxl
import requests
from openpyxl.styles import PatternFill
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Импортируем tqdm для отображения прогресса


def fetch_data(query, page_size, page_end):
    url = f"https://plati.io/api/search.ashx?query={query}&pagesize={page_size}&pagenum={page_end}&visibleOnly=true&response=json"
    response = requests.get(url)
    data = response.json()
    return data.get('items', [])


def extract_account_info(description, title):
    keywords = ["предоставляется аккаунт", "аккаунт предоставляется", "доступ к аккаунту",
                "доступ предоставляется", "остаются на вашем аккаунте", "будет выдан логин и пароль", "Аренда"]
    account_info = "Предоставляется аккаунт" if any(keyword in description.lower() for keyword in keywords) \
                                                or any(keyword in title.lower() for keyword in keywords) else ""
    return account_info + ("Упоминание аккаунта" if "аккаунт" in title.lower() else "")


def add_data_to_excel(query, page_size=500, page_end=10, min_price=None, max_price=None):
    current_time = datetime.now()
    month_folder = current_time.strftime("%B")
    os.makedirs(month_folder, exist_ok=True)
    folder_path = os.path.abspath(month_folder)
    file_name = current_time.strftime(f"{month_folder}/%d_%m_%Y_%H_%M_{query}.xlsx")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["id", "Название", "Цена", "Ссылка", "Платформа", "Продавец", "Рейтинг продавца", "Положительные отзывы",
               "Отрицательные отзывы", "Возвраты", "Упоминание аккаунта"])

    all_items = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_data, query, page_size, page_num) for page_num in range(1, page_end + 1)]
        # Используем tqdm для отображения прогресса выполнения запросов
        for future in tqdm(futures, total=page_end, desc="Fetching data"):
            all_items.extend(future.result())

    if min_price is not None:
        all_items = (item for item in all_items if item.get("price_rur", 0) >= min_price)

    if max_price is not None:
        all_items = (item for item in all_items if item.get("price_rur", 0) <= max_price)

    sorted_items = sorted(all_items, key=lambda x: x.get("price_rur", 0), reverse=True)

    for idx, item in enumerate(sorted_items, start=1):
        name = item.get("name", "")
        price = item.get("price_rur", "")
        url = item.get("url", "")
        title = name.lower()
        platform = next((platform for platform in ["Xbox", "PC", "PS", "Steam"] if platform.lower() in title), "")
        account_info = extract_account_info(item.get("description", ""), title)
        ws.append(
            [item.get("seller_id", ""), name, price, url, platform, item.get("seller_name", ""),
             item.get("seller_rating", ""), item.get("count_positiveresponses", ""),
             item.get("count_negativeresponses", ""), item.get("count_returns", ""), account_info])

        fill = None
        seller_rating = item.get("seller_rating", "")
        if seller_rating < 100:
            fill = PatternFill(start_color="fdc0c8", end_color="fdc0c8", fill_type="solid")
        elif 100 <= seller_rating < 500:
            fill = PatternFill(start_color="fde890", end_color="fde890", fill_type="solid")
        else:
            fill = PatternFill(start_color="c0ecc7", end_color="c0ecc7", fill_type="solid")

        for cell in ws[idx + 1]:
            cell.fill = fill

    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    ws.auto_filter.ref = ws.dimensions
    wb.save(file_name)
    update_info(f"Данные сохранены в файле: {file_name}")
    return folder_path


def open_excel_folder():
    query = query_combobox.get()
    min_price = int(min_price_entry.get() or 0)
    max_price = int(max_price_entry.get() or 0)
    month_folder = add_data_to_excel(query, min_price=min_price, max_price=max_price)
    folder_path = os.path.abspath(month_folder)
    if os.name == 'nt':
        subprocess.Popen(f'explorer "{folder_path}"')
    elif os.name == 'posix':
        subprocess.Popen(['open', folder_path])


def run_query():
    query = query_combobox.get()
    min_price = min_price_entry.get()
    max_price = max_price_entry.get()

    # Проверяем, введены ли значения в поля "От" и "До" цены
    if min_price and max_price:
        min_price = int(min_price)
        max_price = int(max_price)
    else:
        # Используем значение по умолчанию, если не введены
        min_price = None
        max_price = None

    if query:
        info_text.delete(1.0, tk.END)
        add_data_to_excel(query, min_price=min_price, max_price=max_price)
    else:
        update_info("Введите запрос!")


def clear_fields():
    query_combobox.set('')
    min_price_entry.delete(0, tk.END)
    max_price_entry.delete(0, tk.END)


def update_info(message):
    info_text.configure(state=tk.NORMAL)
    info_text.insert(tk.END, message + "\n")
    info_text.configure(state=tk.DISABLED)


root = tk.Tk()
root.title("Добавление данных в Excel")

# Определяем ширину и высоту окна и размещаем его по середине экрана
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Создаем метку и выпадающее меню для запроса
query_label = ttk.Label(root, text="Введите запрос:")
query_label.grid(row=0, column=0, padx=5, pady=5)
query_combobox = ttk.Combobox(root, width=50, style='TCombobox')
query_combobox.grid(row=0, column=1, padx=5, pady=5)

# Создаем рамку для цен
price_frame = ttk.Frame(root)
price_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Метка и поле ввода для минимальной цены
min_price_label = ttk.Label(price_frame, text="Цена от")
min_price_label.grid(row=0, column=0, padx=5, pady=5)
min_price_entry = ttk.Entry(price_frame)
min_price_entry.grid(row=0, column=1, padx=5, pady=5)

# Метка и поле ввода для максимальной цены
max_price_label = ttk.Label(price_frame, text="Цена до")
max_price_label.grid(row=0, column=2, padx=5, pady=5)
max_price_entry = ttk.Entry(price_frame)
max_price_entry.grid(row=0, column=3, padx=5, pady=5)

# Кнопка для запуска запроса
run_button = ttk.Button(root, text="Запустить", command=run_query)
run_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Кнопка для очистки полей
clear_button = ttk.Button(root, text="Очистить", command=clear_fields)
clear_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Кнопка для открытия папки с эксель-файлами
open_folder_button = ttk.Button(root, text="Открыть папку с эксель-файлами", command=open_excel_folder)
open_folder_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Создаем текстовое поле для вывода информации
info_text = tk.Text(root, wrap="word", height=15, width=70)
info_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
info_text.configure(state=tk.DISABLED)

root.mainloop()
