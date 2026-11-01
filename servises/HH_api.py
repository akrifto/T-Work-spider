'''Модуль взаимодействия с API HeadHunter'''

import aiohttp

# HH требует обязательный User-Agent, иначе отдаёт 403
HEADERS = {
    "User-Agent": "JobSpiderBot/1.0 (mytelegrambot@example.com)"
}

HH_API_URL = "https://api.hh.ru/vacancies"


async def fetch_vacancies(text: str = "Python", area: int = 113, per_page: int = 20) -> list:
    """
    Делает запрос к API HH и возвращает сырой список вакансий.
    area=113 - это Россия (можно поменять или вынести в конфиг)
    """
    params = {
        "text": text,
        "area": area,
        "per_page": per_page,
        "order_by": "publication_time",  # Сначала самые свежие!
    }

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        async with session.get(HH_API_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("items", [])
            else:
                # Если HH вернул ошибку (например, лимит или 500)
                print(f"Ошибка HH API: {response.status}")
                return []