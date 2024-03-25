# Добавление данных в Excel

Этот проект представляет собой приложение, которое выполняет поисковые запросы к API и добавляет полученные данные в файл Excel. Программа написана на Python с использованием библиотек Tkinter для создания графического интерфейса пользователя и Openpyxl для работы с файлами Excel.

## Описание

Проект состоит из следующих основных компонентов:

1. **fetch_data**: Функция для получения данных с API. Она отправляет HTTP-запросы к API, основанные на поисковом запросе, и возвращает результаты в формате JSON.

2. **extract_account_info**: Функция для извлечения информации о предоставлении аккаунта. Она анализирует описание и название товара, чтобы определить, предоставляется ли аккаунт в качестве товара.

3. **add_data_to_excel**: Функция для добавления данных в файл Excel. Она использует полученные данные и записывает их в файл Excel с помощью библиотеки Openpyxl. В файле также добавляется информация о предоставлении аккаунта и применяется форматирование для ячеек в зависимости от рейтинга продавца.

4. **open_excel_folder**: Функция для открытия папки с файлами Excel. После выполнения поискового запроса программа сохраняет файл Excel в папке, соответствующей текущему месяцу, и затем открывает эту папку в файловом менеджере.

5. **update_info**: Функция для обновления информации в текстовом поле графического интерфейса. Она добавляет сообщения о состоянии программы, такие как успешное сохранение файла или сообщение об ошибке, в текстовое поле интерфейса.

## Использование 1

1. Запустите программу, запустив файл `api_plati_ru.py`.
2. Введите поисковой запрос в соответствующее поле и нажмите кнопку "Запустить".
3. После завершения выполнения запроса данные будут сохранены в файл Excel.
4. Так же можно использовать кнопку "открыть папку с эксель-файлами" для открытия папки

## Использование 2
1. Зайти в папку dist
2. Запустить exe файл
3. Введите поисковой запрос в соответствующее поле и нажмите кнопку "Запустить"
4. После завершения выполнения запроса данные будут сохранены в файл Excel.
5. Так же можно использовать кнопку "открыть папку с эксель-файлами" для открытия папки

## Зависимости

Для работы программы требуется наличие библиотек Python: `tkinter`, `openpyxl`, `requests`.

##**Примечание**: код создан совместно с chatGPT 

Вы можете установить их, выполнив следующую команду:

```bash
pip install tkinter openpyxl requests



