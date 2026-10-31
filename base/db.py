# db.py

import aiosqlite

DB_NAME = "vacancies.db"

async def init_db():
    """Инициализация БД: создаем таблицы для вакансий и черного списка компаний."""
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица отправленных вакансий
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_vacancies (
                vacancy_id TEXT PRIMARY KEY,
                title TEXT,
                company_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Черный список
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blacklisted_companies (
                company_name TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Избранное
        await db.execute("""
            CREATE TABLE IF NOT EXISTS favorite_companies (
                company_name TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()

async def is_vacancy_sent(vacancy_id: str) -> bool:
    """Защите от дублей"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM sent_vacancies WHERE vacancy_id = ?", (vacancy_id,)
        ) as cursor:
            return await cursor.fetchone() is not None

async def is_company_blacklisted(company_name: str) -> bool:
    """Проверка на ЧС"""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM blacklisted_companies WHERE LOWER(company_name) = LOWER(?)", (company_name,)
        ) as cursor:
            return await cursor.fetchone() is not None

async def add_sent_vacancy(vacancy_id: str, title: str, company_name: str):
    """Запись id, название и компанию"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """INSERT OR IGNORE INTO sent_vacancies (vacancy_id, title, company_name) 
               VALUES (?, ?, ?)""", 
            (vacancy_id, title, company_name)
        )
        await db.commit()

async def add_to_blacklist(company_name: str):
    """Добвыление компании в чс"""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO blacklisted_companies (company_name) VALUES (?)", 
            (company_name,)
        )
        await db.commit()

async def is_company_favorite(company_name: str) -> bool:
    """Проверяем, в избранном ли контора."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT 1 FROM favorite_companies WHERE LOWER(company_name) = LOWER(?)", (company_name,)
        ) as cursor:
            return await cursor.fetchone() is not None

async def add_to_favorites(company_name: str):
    """Добавляем компанию в избранное."""
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR IGNORE INTO favorite_companies (company_name) VALUES (?)", 
            (company_name,)
        )
        await db.commit()

async def remove_from_favorites(company_name: str):
    """Удаляем из избранного, если скатились."""
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "DELETE FROM favorite_companies WHERE LOWER(company_name) = LOWER(?)", 
            (company_name,)):
            await db.commit()