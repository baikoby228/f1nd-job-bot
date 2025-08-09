import telebot
from telebot import types

from dotenv import load_dotenv
import os

from session import get_data, del_data
from user_language import get_user_language, update_user_language
from user_step import set_user_step, del_user_step

from parse import get_links
from translate import translate

from command_processing import (command_start,
                                command_help,
                                command_job,
                                command_language)

from input_processing import input_processing

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def input_command_start(message):
    command_start.processing(message)

@bot.message_handler(commands=['help'])
def input_command_help(message):
    command_help.processing(message)

@bot.message_handler(commands=['job'])
def input_command_job(message):
    command_job.processing(message)

LANGUAGES_LONG = ['Русский', 'Английский', 'Белорусский']
LANGUAGES_SHORT = ['ru', 'en', 'be']

@bot.message_handler(commands=['language'])
def input_command_language(message):
    command_language.processing(message)

@bot.callback_query_handler(func=lambda callback: callback.data in LANGUAGES_SHORT)
def callback_language(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    update_user_language(user_id, callback.data)
    cur_language = get_user_language(user_id)

    long_language_name: str
    for i in range(3):
        if LANGUAGES_SHORT[i] == cur_language:
            long_language_name = LANGUAGES_LONG[i]

    text = (
        f'{translate(f'{long_language_name} выбран \n', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate('для нового запроса', 'ru', cur_language)}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language)}'
    )
    bot.send_message(chat_id, text, parse_mode='html')

is_from_callback = False

@bot.message_handler(content_types=['text'])
def input_text(message):
    input_processing(message)

@bot.callback_query_handler(func=lambda callback: callback.data == 'finished' or '0' <= callback.data <= '4')
def callback_salary(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = get_data(user_id)
    cur_language = get_user_language(user_id)

    if callback.data == 'finished':
        markup = types.InlineKeyboardMarkup(row_width=2)
        b_yes = types.InlineKeyboardButton(translate('Да', 'ru', cur_language), callback_data='Yes')
        b_no = types.InlineKeyboardButton(translate('Нет', 'ru', cur_language), callback_data='No')
        markup.add(b_yes, b_no)

        bot.send_message(chat_id, translate('Показывать объявления без указанной зарплаты?', 'ru', cur_language), parse_mode='html', reply_markup=markup)
        set_user_step(user_id, -1)
        return

    data['cur_type'] = int(callback.data)
    bot.send_message(chat_id, f'{translate('Введите минимальную зарплату в', 'ru', cur_language)} BYN', parse_mode='html')
    set_user_step(user_id, 4)

@bot.callback_query_handler(func=lambda callback: callback.data in ['Yes', 'No'])
def callback_without_salary(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = get_data(user_id)
    cur_language = get_user_language(user_id)

    data['without_salary'] = callback.data == 'Yes'

    data['types_of_work'] = []
    data['desired_salary'] = []
    for i in range(5):
        if i in data and data[i] >= 0:
            data['types_of_work'].append(i)
            data['desired_salary'].append(data[i])

    bot.send_message(chat_id, translate('Все данные получены, сейчас начнёться поиск', 'ru', cur_language), parse_mode='html')
    del_user_step(user_id)
    iterate(callback)
    text = (
        f'{translate('Поиск окончен', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate('для нового запроса', 'ru', cur_language)}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language)}'
    )
    bot.send_message(chat_id, text, parse_mode='html')
    del_data(user_id)

TYPES_OF_YEARS_OF_EXPERIENCE = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
MINIMUM_YEARS_OF_EXPERIENCE = [0, 1, 3]
TYPES_OF_WORK = ['MONTH', 'SHIFT', 'HOUR', 'FLY_IN_FLY_OUT', 'SERVICE']

def iterate(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = get_data(user_id)
    cur_language = get_user_language(user_id)

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

bot.infinity_polling(timeout=60, long_polling_timeout=120)