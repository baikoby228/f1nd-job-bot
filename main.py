import os
from dotenv import load_dotenv
import telebot
from telebot import types
from job import job_process

from parse import get
from find_number import find_number
from translate import translate, translate_job, translate_city

from session import get_data, del_data
from user_language import get_user_language, update_user_language

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

LANGUAGES_LONG = ['Русский', 'Английский', 'Белорусский']
LANGUAGES_SHORT = ['ru', 'en', 'be']
TYPES_OF_WORK_RU = ['За месяц', 'За смену', 'За час', 'За вахту', 'За услугу']
TYPES_OF_YEARS_OF_EXPERIENCE = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
MINIMUM_YEARS_OF_EXPERIENCE = [0, 1, 3]
TYPES_OF_WORK = ['MONTH', 'SHIFT', 'HOUR', 'FLY_IN_FLY_OUT', 'SERVICE']
is_from_callback = False


@bot.message_handler(commands=['start'])
def start(message):
    language = get_user_language(message.from_user.id)

    text = (
        f'{translate('Привет! Я дам все вакансии на rabota.by по заданным критериям', 'ru', language)}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', language)}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', language)}'
    )
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
    language = get_user_language(message.from_user.id)

    text = (
        f'<code>/start</code> {translate(' я расскажу о себе', 'ru', language)}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', language)}\n'
        f'<code>/language</code> {translate(' для смены языка', 'ru', language)}'
    )
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['job'])
def job(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    job_process(bot, user_id, chat_id)


@bot.message_handler(commands=['language'])
def change_language(message):
    language = get_user_language(message.from_user.id)

    markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(3):
        b = types.InlineKeyboardButton(translate(LANGUAGES_LONG[i], 'ru', language), callback_data=LANGUAGES_SHORT[i])
        markup.add(b)

    bot.send_message(message.chat.id, translate('Выберите нужный язык', 'ru', language), parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in LANGUAGES_SHORT)
def callback_change_language(callback):
    update_user_language(callback.from_user.id, callback.data)
    language = get_user_language(callback.from_user.id)

    long_language_name: str
    for i in range(3):
        if LANGUAGES_SHORT[i] == language:
            long_language_name = LANGUAGES_LONG[i]

    text = (
        f'{translate(f'{long_language_name} выбран \n', 'ru', language)}\n'
        f'<code>/start</code> {translate('для нового запроса', 'ru', language)}'
    )
    bot.send_message(callback.message.chat.id, text, parse_mode='html')


@bot.message_handler(content_types=['text'])
def info_processing(message):
    data = get_data(message.from_user.id)
    language = get_user_language(message.from_user.id)

    if 'step' in data:
        match data['step']:
            case 0:
                data['desired_job'] = translate_job(message.text, language)
                bot.send_message(message.chat.id, translate('Введите название города', 'ru', language), parse_mode='html')
                data['step'] += 1
            case 1:
                data['desired_city'] = translate_city(message.text)
                bot.send_message(message.chat.id, translate('Введите количество лет опыта работы в этой профессии', 'ru', language), parse_mode='html')
                data['step'] += 1
            case 2:
                data['years_of_experience'] = int(find_number(message.text))

                flag = False
                markup = types.InlineKeyboardMarkup()
                for i in range(5):
                    b = types.InlineKeyboardButton(f'{translate(TYPES_OF_WORK_RU[i], 'ru', language)}: {'-' if data[i] < 0 else data[i]}', callback_data=str(i))
                    markup.add(b)
                    flag |= data[i] >= 0

                dop = ''
                if flag:
                    b = types.InlineKeyboardButton(translate('Готово!', 'ru', language), callback_data='finished')
                    markup.add(b)
                    dop = 'Если введённые данные верны нажмите Готово!'

                bot.send_message(message.chat.id, translate(f'Выберите типы оплаты {dop}', 'ru', language), parse_mode='html', reply_markup=markup)
            case 3:
                data[int(data['cur_type'])] = int(find_number(message.text))
                data['step'] -= 1
                info_processing(message)


@bot.callback_query_handler(func=lambda call: call.data == 'finished' or '0' <= call.data <= '4')
def callback_salary(callback):
    data = get_data(callback.from_user.id)
    language = get_user_language(callback.from_user.id)

    if callback.data == 'finished':
        markup = types.InlineKeyboardMarkup(row_width=2)
        b_yes = types.InlineKeyboardButton(translate('Да', 'ru', language), callback_data='Yes')
        b_no = types.InlineKeyboardButton(translate('Нет', 'ru', language), callback_data='No')
        markup.add(b_yes, b_no)

        bot.send_message(callback.message.chat.id, translate('Показывать объявления без указанной зарплаты?', 'ru', language), parse_mode='html', reply_markup=markup)
        return

    data['cur_type'] = int(callback.data)
    bot.send_message(callback.message.chat.id, f'{translate('Введите минимальную зарплату в', 'ru', language)} BYN', parse_mode='html')
    data['step'] += 1


@bot.callback_query_handler(func=lambda call: call.data in ['Yes', 'No'])
def callback_without_salary(callback):
    data = get_data(callback.from_user.id)
    language = get_user_language(callback.from_user.id)

    data['without_salary'] = callback.data == 'Yes'

    data['types_of_work'] = []
    data['desired_salary'] = []
    for i in range(5):
        if i in data and data[i] >= 0:
            data['types_of_work'].append(i)
            data['desired_salary'].append(data[i])

    bot.send_message(callback.message.chat.id, translate('Все данные получены, сейчас начнёться поиск', 'ru', language), parse_mode='html')
    iterate(callback)
    bot.send_message(callback.message.chat.id, f'{translate('Поиск окончен', 'ru', language)}\n<code>/start</code> {translate('для нового запроса', 'ru', language)}', parse_mode='html')
    del_data(callback.from_user.id)


def iterate(callback):
    data = get_data(callback.from_user.id)
    language = get_user_language(callback.from_user.id)

    for i in range(len(MINIMUM_YEARS_OF_EXPERIENCE)):
        if data['years_of_experience'] >= MINIMUM_YEARS_OF_EXPERIENCE[i]:
            for j in range(len(data['types_of_work'])):
                res = get(language, data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[i], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
                for vacancy in res:
                    bot.send_message(callback.message.chat.id, vacancy, parse_mode='html')

    if data['years_of_experience'] >= 6:
        for j in range(len(data['types_of_work'])):
            res = get(language, data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[-1], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
            for vacancy in res:
                bot.send_message(callback.message.chat.id, vacancy, parse_mode='html')


bot.infinity_polling(timeout=60, long_polling_timeout=120)