'''Модуль прямого взаимодействия с API HeadHunter без фильтров'''

import aiohttp

HH_API_URL = "https://api.hh.ru/vacancies"
HEADERS = {
    "User-Agent": "WorkSpiderBot/1.0 (admin@workspider.local)"
}

# Регионы: Минск (1002), Беларусь (16), Россия (113)
DEFAULT_AREAS = [1002, 16, 113]


async def hh_fetch() -> list[dict]:
    '''Делает прямой запрос к API HH по ключевым регионам без лишних фильтров'''
    all_vacancies = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for area_id in DEFAULT_AREAS:
            params = {
                "per_page": 20,
                "order_by": "publication_time",
                "area": area_id
            }
            
            try:
                async with session.get(HH_API_URL, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("items", [])
                        all_vacancies.extend(items)
            except Exception:
                pass

    return all_vacancies