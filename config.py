# config.py

import os
from dotenv import load_dotenv

load_dotenv()  

BOT_TOKEN = os.getenv("BOT_TOKEN")


class  Filter:
    '''Единый контейнер фильтров поиска'''

    class Global:
        '''API HH, префильтр'''

        # Вот тут я тупанул, оно не создавалось
        def __init__(self):
            self.key_word: list[str] = []
            self.active_region: list[int] = []
            self.active_shedule: str = ''
            self.active_skill: str = ''
            self.active_employment: str = ''
            self.salary: int = 0
            self.salary_only: bool = False

        # Вся Россия и Беларусь для удаленки. Минск будет для оффлайн работы 
        region: dict[str, int] = {
            'Минск': 1002,
            'Вся Беларусь': 16,
            'Вся Россия': 113,
        }

        shedule: dict[str, str] = {
            'Полный день': 'fullDay',
            'Сменный график': 'shift',
            'Гибкий график': 'flexible',
            'Удалённая работа': 'remote',
            'Вахтовый метод': 'flyInFlyOut',
        }

        skill: dict[str, str] = {
            'Нет опыта': 'noExperience',
            'От 1 года до 3 лет': 'between1And3',
            'От 3 до 6 лет': 'between3And6',
            'Более 6 лет': 'moreThan6',
        }

        employment: dict[str, str] = {
            'Полная занятость': 'full',
            'Частичная занятость': 'part',
            'Подработка': 'project',
        }

    class Local:
        '''Локальные фильтры, постфильтр'''

        def __init__(self):
            self.ban_word: list[str] = []
            self.active_exact_schedule: list[str] = []
            self.active_salary_frec: list[str] = [] 
            self.dogovor_gph: bool = False # Флаг ГПХ

        # График работы
        exact_schedule: tuple[str, ...] = (
            '6/1', '5/2', '4/4', '4/3', '4/2',
            '3/3', '3/2', '2/2', '2/1', '1/3', '1/2',
            'По выходным', 'Свободный',
        )

        # Частота выплат
        salary_frec: tuple[str, ...] = (
            'За проект',
            'Ежедневно',
            'Раз в неделю',
            'Два раза в месяц',
            'Раз в месяц',
        )

        # Словарь для отлова вакансий с ГПХ/СЗ (По необходимости буду дописывать)
        gph_terms = [ 
            'гпх', 
            'самозанятый',
            'самозанятым', 
            'сз', 
            'подряд',
            'подряду',
            'подряда',
            ]