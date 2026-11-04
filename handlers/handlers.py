'''Модуль обработки команд и callback-запросов бота'''

import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InaccessibleMessage
from aiogram.filters import Command

from servises.HH_api import hh_fetch
from keyboards.keyboards import get_vacancy_keyboard
from base.db import Base, BlackList

router = Router()

# Хранилище фоновых задач по user_id
user_tasks: dict[int, asyncio.Task] = {}


async def fetch_and_send_vacancies(bot, user_id: int):
    '''Основная логика запроса, проверки дублей и отправки вакансий'''
    await Base.init()
    
    raw_vacancies = await hh_fetch()
    if not raw_vacancies:
        return 0

    sent_count = 0
    for item in raw_vacancies:
        vacancy_id = str(item.get("id"))
        title = item.get("name", "Без названия")
        employer = item.get("employer", {}).get("name", "Неизвестно")
        
        # Проверяем черный список
        if await BlackList.check(employer):
            continue

        # Защита от дублей через БД
        if await Base.doble_security(vacancy_id):
            continue
        
        # Сохраняем в базу
        await Base.add(vacancy_id, title, employer)
        sent_count += 1
        
        salary_data = item.get("salary")
        if salary_data:
            sal_from = salary_data.get("from")
            sal_to = salary_data.get("to")
            currency = salary_data.get("currency", "RUR")
            salary_str = f"{sal_from or 'от'} - {sal_to or 'до'} {currency}"
        else:
            salary_str = "Зарплата не указана"
            
        url = item.get("alternate_url", "")
        
        text = (
            f"🔥 **{title}**\n"
            f"🏢 Компания: {employer}\n"
            f"💰 {salary_str}"
        )
        
        await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=get_vacancy_keyboard(url),
            parse_mode="Markdown"
        )
    return sent_count


async def background_loop(bot, user_id: int):
    '''Фоновый цикл проверки вакансий каждую 1 минуту'''
    while True:
        try:
            await fetch_and_send_vacancies(bot, user_id)
        except Exception:
            pass
        await asyncio.sleep(60)


@router.message(Command("start"))
async def cmd_start(message: Message):
    '''Старт работы бота и запуск минутного мониторинга'''
    if not message.from_user:
        return

    user_id = message.from_user.id
    await Base.init()

    await message.answer(
        "Здарова, бро. WorkSpider запущен.\n"
        "Мониторю свежие вакансии по Минску, Беларуси и России каждую 1 минуту 🕷️"
    )

    # Отменяем старую задачу, если была
    if user_id in user_tasks and not user_tasks[user_id].done():
        user_tasks[user_id].cancel()

    # Сразу делаем первый поиск при старте
    await fetch_and_send_vacancies(message.bot, user_id)

    # Запускаем фоновый таймер на 1 минуту
    user_tasks[user_id] = asyncio.create_task(
        background_loop(message.bot, user_id)
    )


@router.callback_query(F.data == "fetch_more")
async def process_fetch_more(callback: CallbackQuery):
    '''Принудительный поиск по клику на кнопку "Смотреть дальше"'''
    if not callback.message or isinstance(callback.message, InaccessibleMessage):
        await callback.answer()
        return

    user_id = callback.from_user.id
    await callback.answer("Ищу свежак...")

    count = await fetch_and_send_vacancies(callback.bot, user_id)
    
    if count == 0:
        await callback.message.answer("Новых вакансий пока нет, бро. Ждём следующий цикл.")