# config.py

import os
from dotenv import load_dotenv

load_dotenv()  

BOT_TOKEN = os.getenv("BOT_TOKEN")


class Filter:
    '''Единый контейнер фильтров поиска'''

    class Global:
        '''API HH, префильтр'''

        key_word: list[str] = []

        # Регионы
        region: dict[str, int] = {
            'Минск': 1002,
            'Вся Беларусь': 16,
            'Вся Россия': 113,
        }
        active_region: list[int] = []

        # График работы
        shedule: dict[str, str] = {
            'Полный день': 'fullDay',
            'Сменный график': 'shift',
            'Гибкий график': 'flexible',
            'Удалённая работа': 'remote',
            'Вахтовый метод': 'flyInFlyOut',
        }
        active_shedule: str = 'shift'

        # Требуемый опыт работы 
        skill: dict[str, str] = {
            'Нет опыта': 'noExperience',
            'От 1 года до 3 лет': 'between1And3',
            'От 3 до 6 лет': 'between3And6',
            'Более 6 лет': 'moreThan6',
        }
        active_skill: str = 'noExperience'

        # Формат работы 
        format: dict[str, str] = {
            'На месте работодателя': 'fullDay',
            'Удалённо': 'remote',
            'Гибрид': 'flexible',
            'Разъездной': 'flyInFlyOut',
        }
        active_format: str = 'remote'

        # Тип занятости
        employment: dict[str, str] = {
            'Полная занятость': 'full',
            'Частичная занятость': 'part',
            'Подработка': 'project',
        }
        active_employment: str = 'full'

        # Зарплатные настройки
        salary: int = 0 # Минимальное ЗП
        salary_only: bool = False # Флаг указанного ЗП

    class Local:
        '''Локальные фильтры, постфильтр'''

        # Стоп-слова (ищем в заголовках и описании)
        ban_word: list[str] = []

        # Жесткие графики смен (поиск по текстовке)
        exact_schedule: tuple[str, ...] = (
            '6/1', '5/2', '4/4', '4/3', '4/2',
            '3/3', '3/2', '2/2', '2/1', '1/3', '1/2',
            'По выходным', 'Свободный', 
        )
        active_exact_schedule: str = ''

        # Частота выплат
        salary_frec: tuple[str, ...] = (
            'За проект',
            'Ежедневно',
            'Раз в неделю',
            'Два раза в месяц',
            'Раз в месяц',
        )
        active_salary_frec: str = ''

        # Работа по ГПХ/СЗ/совместительство
        dogovor_gph: bool = False
