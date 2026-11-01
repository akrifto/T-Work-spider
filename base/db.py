# db.py

'''Действия с бд'''

import aiosqlite

DB_NAME = "vacancies.db"


class Base:
    '''Основное бд'''

    @staticmethod
    async def init():
        """создание таблицы"""
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

    @staticmethod
    async def doble_security(vacancy_id: str) -> bool:
        """Защите от дублей"""
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute(
                "SELECT 1 FROM sent_vacancies WHERE vacancy_id = ?", (vacancy_id,)
            ) as cursor:
                return await cursor.fetchone() is not None

    @staticmethod
    async def add(vacancy_id: str, title: str, company_name: str):
        """Запись id, название и компанию"""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                """INSERT OR IGNORE INTO sent_vacancies (vacancy_id, title, company_name) 
                   VALUES (?, ?, ?)""", 
                (vacancy_id, title, company_name)
            )
            await db.commit()

    @staticmethod
    async def clear_old(days: int = 30):
        """Очистка вакансий старше указанного количества дней (по дефолту 30)"""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "DELETE FROM sent_vacancies WHERE created_at < DATETIME('now', ? || ' days')",
                (f"-{days}",)
            )
            await db.commit()

class BlackList:
    '''Черный список'''

    @staticmethod
    async def check(company_name: str) -> bool:
        """Проверка на ЧС"""
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute(
                "SELECT 1 FROM blacklisted_companies WHERE LOWER(company_name) = LOWER(?)", (company_name,)
            ) as cursor:
                return await cursor.fetchone() is not None

    @staticmethod
    async def add(company_name: str):
        """Добвыление компании в чс"""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "INSERT OR IGNORE INTO blacklisted_companies (company_name) VALUES (?)", 
                (company_name,)
            )
            await db.commit()

    


class WhiteList:
    '''Избранные компании (вайтлист)'''

    @staticmethod
    async def check(company_name: str) -> bool:
        """Проверка на наличие в мзбранном"""

        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute(
                "SELECT 1 FROM favorite_companies WHERE LOWER(company_name) = LOWER(?)", (company_name,)
            ) as cursor:
                return await cursor.fetchone() is not None

    @staticmethod
    async def add(company_name: str):
        """Добавляем компанию в избранное."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "INSERT OR IGNORE INTO favorite_companies (company_name) VALUES (?)", 
                (company_name,)
            )
            await db.commit()

    @staticmethod
    async def remove(company_name: str):
        """Удаляем из избранного, если скатились."""
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute(
                "DELETE FROM favorite_companies WHERE LOWER(company_name) = LOWER(?)", 
                (company_name,)
            )
            await db.commit()