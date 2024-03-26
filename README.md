
Добавление данных в Excel
Этот проект представляет собой приложение, которое выполняет поисковые запросы к API и добавляет полученные данные в файл Excel. Программа написана на Python с использованием библиотек Tkinter для создания графического интерфейса пользователя и Openpyxl для работы с файлами Excel.

Описание
Проект состоит из следующих основных компонентов:

fetch_data: Функция для получения данных с API. Она отправляет HTTP-запросы к API, основанные на поисковом запросе, и возвращает результаты в формате JSON.

extract_account_info: Функция для извлечения информации о предоставлении аккаунта. Она анализирует описание и название товара, чтобы определить, предоставляется ли аккаунт в качестве товара.

add_data_to_excel: Функция для добавления данных в файл Excel. Она использует полученные данные и записывает их в файл Excel с помощью библиотеки Openpyxl. В файле также добавляется информация о предоставлении аккаунта и применяется форматирование для ячеек в зависимости от рейтинга продавца.

open_excel_folder: Функция для открытия папки с файлами Excel. После выполнения поискового запроса программа сохраняет файл Excel в папке, соответствующей текущему месяцу, и затем открывает эту папку в файловом менеджере.

update_info: Функция для обновления информации в текстовом поле графического интерфейса. Она добавляет сообщения о состоянии программы, такие как успешное сохранение файла или сообщение об ошибке, в текстовое поле интерфейса.

Использование
Запуск программы из исходного кода:

Запустите программу, запустив файл api_plati_ru.py.
Введите поисковой запрос в соответствующее поле и нажмите кнопку "Запустить".
После завершения выполнения запроса данные будут сохранены в файл Excel.
Используйте кнопку "Открыть папку с эксель-файлами", чтобы открыть папку с сохраненными файлами.
Запуск программы из скомпилированного исполняемого файла:

Зайдите в папку dist.
Запустите .exe файл.
Введите поисковой запрос в соответствующее поле и нажмите кнопку "Запустить".
После завершения выполнения запроса данные будут сохранены в файл Excel.
Используйте кнопку "Открыть папку с эксель-файлами", чтобы открыть папку с сохраненными файлами.
Пример автотеста
Пример автотеста для проверки API можно найти в файле test_main.py.

Зависимости
Для работы программы требуется наличие библиотек Python: tkinter, openpyxl, requests.

Примечание
Код разработан с использованием совместно с ChatGPT.
