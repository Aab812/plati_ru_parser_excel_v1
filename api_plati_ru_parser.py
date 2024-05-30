import requests


def api_platti_ru_from_developers():
    #{поисковая_фраза} — не менее трех символов
    #{товаров настранице} — 20 по умолчанию;неболее 500
    #{номер страницы} — используется, когда первоначальный запрос вернул totalpages больше 1
    #{только доступные} — только доступные для покупки: true | false
    #{формат ответа} — xml/json, xml по умолчанию

    search = "spider-man-2"
    couts = 500
    number_page = 1
    access = True
    formatus = "json"

    url = (f"https://plati.io/api/search.ashx?query={search}&pagesize={couts}&pagenum={number_page}&visibleOnly={access}&response={formatus}")
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)

    return response

