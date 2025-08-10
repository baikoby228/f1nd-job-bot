import telebot

from dotenv import load_dotenv
import os

from parse import get_links

from user_step import del_user_step

from session import get_data, del_data
from translate import translate
from user_language import get_user_language

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

TYPES_OF_YEARS_OF_EXPERIENCE = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
MINIMUM_YEARS_OF_EXPERIENCE = [0, 1, 3]
TYPES_OF_WORK = ['MONTH', 'SHIFT', 'HOUR', 'FLY_IN_FLY_OUT', 'SERVICE']

def iterate(user_id, chat_id):
    cur_language = get_user_language(user_id)
    data = get_data(user_id)

    bot.send_message(chat_id, translate('Все данные получены, сейчас начнёться поиск', 'ru', cur_language), parse_mode='html')

    for i in range(len(MINIMUM_YEARS_OF_EXPERIENCE)):
        if data['years_of_experience'] >= MINIMUM_YEARS_OF_EXPERIENCE[i]:
            for j in range(len(data['types_of_work'])):
                res = get_links(cur_language, data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[i], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
                for vacancy in res:
                    bot.send_message(chat_id, vacancy, parse_mode='html')

    if data['years_of_experience'] >= 6:
        for j in range(len(data['types_of_work'])):
            res = get_links(cur_language, data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[-1], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
            for vacancy in res:
                bot.send_message(chat_id, vacancy, parse_mode='html')

    text = (
        f'{translate('Поиск окончен', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate('для нового запроса', 'ru', cur_language).lower()}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')

    del_data(user_id)
    del_user_step(user_id)