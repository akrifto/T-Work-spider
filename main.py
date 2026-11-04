import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.handlers import router as lego_router

async def main():
    """
    Главная асинхронная точка входа: инициализирует бота,
    подключает роутеры и запускает поллинг обновлений.
    """
    if not isinstance(BOT_TOKEN, str) or not BOT_TOKEN:
        raise ValueError("BOT_TOKENа нету или это не строка")
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(lego_router)
    
    print("Есть контакт")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())