import telebot

from dotenv import load_dotenv
import os

from session import get_user
from parse import get_links
from translate import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

TYPES_OF_YEARS_OF_EXPERIENCE = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
MINIMUM_YEARS_OF_EXPERIENCE = [0, 1, 3]
TYPES_OF_WORK = ['MONTH', 'SHIFT', 'HOUR', 'FLY_IN_FLY_OUT', 'SERVICE']

def iterate(user_id, chat_id) -> None:
    user = get_user(user_id)
    cur_language = user.language

    bot.send_message(chat_id, translate('Все данные получены, сейчас начнёться поиск', 'ru', cur_language), parse_mode='html')

    user.types_of_work = []
    user.desired_salary = []
    for i in range(5):
        if user.desired_types[i] >= 0:
            user.types_of_work.append(i)
            user.desired_salary.append(user.desired_types[i])

    for i in range(len(MINIMUM_YEARS_OF_EXPERIENCE)):
        if user.years_of_experience >= MINIMUM_YEARS_OF_EXPERIENCE[i]:
            for j in range(len(user.types_of_work)):
                res = get_links(cur_language, user.desired_job, user.desired_city, TYPES_OF_YEARS_OF_EXPERIENCE[i], TYPES_OF_WORK[user.types_of_work[j]], user.desired_salary[j], user.without_salary)
                for vacancy in res:
                    bot.send_message(chat_id, vacancy, parse_mode='html')

    if user.years_of_experience >= 6:
        for j in range(len(user.types_of_work)):
            res = get_links(cur_language, user.desired_job, user.desired_city, TYPES_OF_YEARS_OF_EXPERIENCE[-1], TYPES_OF_WORK[user.types_of_work[j]], user.desired_salary[j], user.without_salary)
            for vacancy in res:
                bot.send_message(chat_id, vacancy, parse_mode='html')

    text = (
        f'{translate('Поиск окончен', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate('для нового запроса', 'ru', cur_language).lower()}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')