# main.py

import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router as lego_router

async def main():
    """
    Главная асинхронная точка входа: инициализирует бота,
    подключает роутеры и запускает поллинг обновлений.
    """
    # Проверяем наличие и валидность токена
    if not isinstance(BOT_TOKEN, str) or not BOT_TOKEN:
        raise ValueError("BOT_TOKENа нету или это не строка") # По сути чисто формальность
    
    # Инициализация бота и диспетчера
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем модуль-роутер
    dp.include_router(lego_router)
    
    print("Есть контакт")
    await dp.start_polling(bot)

# Просто этикет
if __name__ == "__main__":
    asyncio.run(main())