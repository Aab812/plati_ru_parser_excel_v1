# Импорт модуля для взаимодействия с операционной системой
import os

# Модуль для запуска дочерних процессов
import subprocess

# Модуль для создания графического интерфейса
import tkinter as tk

# Модуль для работы с датой и временем
from datetime import datetime

# Модуль для создания дополнительных виджетов в tkinter
from tkinter import ttk

# Модуль для работы с файлами Excel
import openpyxl

# Модуль для отправки HTTP-запросов
import requests

# Модуль для работы со стилями Excel
from openpyxl.styles import PatternFill


def fetch_data(query, page_size, page_num):
    """
    Функция для получения данных с API.

    Args:
        query: Строка, содержащая поисковый запрос.
        page_size: Количество элементов на странице.
        page_num: Номер страницы.

    Returns:
        Кортеж из списка элементов и общего количества элементов.
    """
    # Формирование URL для запроса к API
    url = f"https://plati.io/api/search.ashx?query={query}&pagesize={page_size}&pagenum={page_num}&visibleOnly=true&response=json"

    # Отправка GET-запроса к API
    response = requests.get(url)

    # Преобразование ответа в формат JSON и возвращение результатов
    data = response.json()
    return data['items'], data['total']


def extract_account_info(description, title):
    """
    Функция для извлечения информации о предоставлении аккаунта.

    Args:
        description: Описание товара.
        title: Заголовок товара.

    Returns:
        Строка, описывающая информацию о предоставлении аккаунта.
    """
    # Ключевые слова, указывающие на предоставление аккаунта
    keywords = ["предоставляется аккаунт", "аккаунт предоставляется", "доступ к аккаунту",
                "доступ предоставляется", "Остаются на Вашем аккаунте", "будет выдан логин и пароль"]

    account_info = ""  # Переменная для хранения информации о предоставлении аккаунта

    # Проверка наличия ключевых слов в описании или заголовке товара
    if any(keyword in description.lower() for keyword in keywords):
        account_info = "Предоставляется аккаунт"
    elif "offline" in title.lower() or "оффлайн" in title.lower():
        account_info = "Предоставляется аккаунт"

    return account_info  # Возвращение информации о предоставлении аккаунта
def add_data_to_excel(query, page_size=500, page_end=10):
    """
    Функция для добавления данных в файл Excel.

    Args:
        query: Строка, содержащая поисковый запрос.
        page_size: Количество элементов на странице.
        page_end: Количество страниц для поиска.

    Returns:
        Путь к папке с сохраненными файлами Excel.
    """
    # Получение текущего времени
    current_time = datetime.now()

    # Получение названия текущего месяца
    month_folder = current_time.strftime("%B")

    # Создание папки для текущего месяца (если не существует)
    os.makedirs(month_folder, exist_ok=True)

    # Получение абсолютного пути к папке
    folder_path = os.path.abspath(month_folder)

    # Формирование имени файла
    file_name = current_time.strftime(f"{month_folder}/%d_%m_%Y_%H_%M_{query}.xlsx")

    # Создание нового документа Excel
    wb = openpyxl.Workbook()

    # Получение активного листа
    ws = wb.active

    # Запись заголовков столбцов в файл Excel
    ws.append(["id", "Название", "Цена", "Ссылка", "Платформа", "Продавец", "Рейтинг продавца", "Положительные отзывы",
               "Отрицательные отзывы", "Возвраты", "Упоминание аккаунта"])

    all_items = []  # Создание пустого списка для хранения всех элементов
    total_items = 0  # Инициализация переменной для общего количества элементов

    # Поиск элементов на нескольких страницах
    for page_num in range(1, page_end + 1):
        items, total = fetch_data(query, page_size, page_num)  # Получение данных с API
        total_items = total  # Обновление общего количества элементов
        all_items.extend(items)  # Добавление полученных элементов в общий список

    sorted_items = sorted(all_items, key=lambda x: x.get("price_rur", 0), reverse=True)  # Сортировка элементов по цене

    # Запись данных в файл Excel
    for idx, item in enumerate(sorted_items, start=1):
        # Извлечение данных об элементе
        name = item.get("name", "")
        price = item.get("price_rur", "")
        url = item.get("url", "")
        platform = ""
        seller_id = item.get("seller_id", "")
        seller_name = item.get("seller_name", "")
        seller_rating = item.get("seller_rating", "")
        positive_responses = item.get("count_positiveresponses", "")
        negative_responses = item.get("count_negativeresponses", "")
        returns = item.get("count_returns", "")
        description = item.get("description", "")

        # Определение платформы
        title = name.lower()
        if "xbox" in title:
            platform = "Xbox"
        elif "pc" in title:
            platform = "PC"
        elif "ps" in title:
            platform = "PS"
        elif "steam" in title:
            platform = "Steam"

        account_info = extract_account_info(description, title)  # Извлечение информации о предоставлении аккаунта

        # Запись данных в файл Excel
        ws.append(
            [seller_id, name, price, url, platform, seller_name, seller_rating, positive_responses, negative_responses,
             returns, account_info])

        # Установка заливки ячеек в зависимости от рейтинга продавца
        fill = None
        if seller_rating < 100:
            fill = PatternFill(start_color="fdc0c8", end_color="fdc0c8", fill_type="solid")
        elif 100 <= seller_rating < 500:
            fill = PatternFill(start_color="fde890", end_color="fde890", fill_type="solid")
        else:
            fill = PatternFill(start_color="c0ecc7", end_color="c0ecc7", fill_type="solid")

        for cell in ws[idx + 1]:  # Применение заливки к ячейкам
            cell.fill = fill

    # Настройка ширины столбцов
    for column_cells in ws.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 2

    ws.auto_filter.ref = ws.dimensions  # Применение фильтра к таблице

    wb.save(file_name)  # Сохранение файла Excel
    update_info(f"Данные сохранены в файле: {file_name}")  #

    # Вывод информации в текстовое поле
    return folder_path  # Возвращение пути к папке с файлами Excel

def open_excel_folder():
    """
    Функция для открытия папки с файлами Excel.
    """
    # Получение пути к папке с файлами Excel
    month_folder = add_data_to_excel(query_combobox.get())
    folder_path = os.path.abspath(month_folder)

    # Открытие папки в файловом менеджере в зависимости от операционной системы
    if os.name == 'nt':  # Если это Windows
        subprocess.Popen(f'explorer "{folder_path}"')
    elif os.name == 'posix':  # Если это macOS
        subprocess.Popen(['open', folder_path])

def update_info(message):
    """
    Функция для обновления информации в текстовом поле.

    Args:
        message: Сообщение, которое нужно добавить в текстовое поле.
    """
    # Включение возможности редактирования текстового поля
    info_text.configure(state=tk.NORMAL)
    # Добавление сообщения в текстовое поле
    info_text.insert(tk.END, message + "\n")
    # Отключение возможности редактирования текстового поля
    info_text.configure(state=tk.DISABLED)
    # Прокрутка текстового поля к концу
    info_text.see(tk.END)

def run_query():
    """
    Функция для выполнения поискового запроса.
    """
    # Получение текста из поля ввода
    query = query_combobox.get()

    if query:  # Если запрос не пустой
        # Очистка текстового поля
        info_text.delete(1.0, tk.END)
        # Вызов функции добавления данных в файл Excel
        add_data_to_excel(query)
    else:
        # Вывод сообщения об ошибке, если запрос пустой
        update_info("Введите запрос!")

# Создание главного окна приложения
root = tk.Tk()

# Установка заголовка окна
root.title("Добавление данных в Excel")

# Размеры и позиция окна
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Метка для ввода запроса
query_label = ttk.Label(root, text="Введите запрос:")
query_label.pack(pady=10)

# Поле для ввода запроса
query_combobox = ttk.Combobox(root, width=50, style='TCombobox')
query_combobox.pack()

# Кнопка для выполнения поискового запроса
run_button = ttk.Button(root, text="Запустить", command=run_query)
run_button.pack(pady=10)

# Кнопка для открытия папки с файлами Excel
open_folder_button = ttk.Button(root, text="Открыть папку с эксель-файлами", command=open_excel_folder)
open_folder_button.pack(pady=10)

# Текстовое поле для вывода информации
info_text = tk.Text(root, wrap="word", height=15, width=70)
info_text.pack(pady=10)
info_text.configure(state=tk.DISABLED)

root.mainloop()
