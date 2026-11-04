'''Модуль генерации инлайн-клавиатур'''

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_vacancy_keyboard(url: str) -> InlineKeyboardMarkup:
    '''Кнопка со ссылкой на вакансию и кнопка "Смотреть дальше"'''
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Ознакомиться 🔗", url=url))
    builder.row(InlineKeyboardButton(text="Смотреть дальше ➡️", callback_data="fetch_more"))
    return builder.as_markup()