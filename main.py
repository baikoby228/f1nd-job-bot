#pip install requests, fake_useragent, bs4, lxml
#pip install telebot
#pip install python-dotenv

import telebot
from dotenv import load_dotenv
from telebot import types

from parse import get
from find_number import find_number

import dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

session = {}

@bot.message_handler(commands=['start'])
def start(message):
    session[message.from_user.id] = {}
    data = session[message.from_user.id]

    data['step'] = 0
    for x in range(5):
        data[x] = -1

    bot.send_message(message.chat.id, 'Привет! Я дам все вакансии на rabota.by', parse_mode='html')
    bot.send_message(message.chat.id, 'Введите профессию', parse_mode='html')

TYPES_OF_WORK_RU = ['месяц', 'смену', 'час', 'вахту', 'услугу']
is_from_callback = False

@bot.message_handler(content_types=['text'])
def info_processing(message):
    data = session[message.from_user.id]

    match data['step']:
        case 0:
            data['desired_job'] = message.text
            bot.send_message(message.chat.id, 'Введите название города', parse_mode='html')
            data['step'] += 1
        case 1:
            data['desired_city'] = message.text
            bot.send_message(message.chat.id, 'Введите количество лет опыта работы в этой профессии', parse_mode='html')
            data['step'] += 1
        case 2:
            data['years_of_experience'] = int(find_number(message.text))

            flag = False
            markup = types.InlineKeyboardMarkup()
            for i in range(5):
                b = types.InlineKeyboardButton(f'За {TYPES_OF_WORK_RU[i]}: {'-' if data[i] < 0 else data[i]}', callback_data=str(i))
                markup.add(b)
                flag |= data[i] >= 0

            dop = ''
            if flag:
                b = types.InlineKeyboardButton('Готово!', callback_data='finished')
                markup.add(b)
                dop = 'Если введённые данные верны нажмите Готово!'

            bot.send_message(message.chat.id, f'Выберите типы оплаты {dop}', parse_mode='html', reply_markup=markup)
        case 3:
            data[int(data['cur_type'])] = int(find_number(message.text))
            data['step'] -= 1
            info_processing(message)

@bot.callback_query_handler(func=lambda call: call.data == 'finished' or '0' <= call.data <= '4')
def callback_salary(callback):
    data = session[callback.from_user.id]

    if callback.data == 'finished':
        markup = types.InlineKeyboardMarkup(row_width=2)
        b_yes = types.InlineKeyboardButton('Да', callback_data='Yes')
        b_no = types.InlineKeyboardButton('Нет', callback_data='No')
        markup.add(b_yes, b_no)

        bot.send_message(callback.message.chat.id, 'Показывать объявления без указанной зп?', parse_mode='html', reply_markup=markup)
        return

    data['cur_type'] = int(callback.data)
    bot.send_message(callback.message.chat.id, 'Введите минимальную зп в BYN', parse_mode='html')
    data['step'] += 1

@bot.callback_query_handler(func=lambda call: call.data in ['Yes', 'No'])
def callback_without_salary(callback):
    data = session[callback.from_user.id]

    data['without_salary'] = callback.data == 'Yes'

    data['types_of_work'] = []
    data['desired_salary'] = []
    for i in range(5):
        if data[i] >= 0:
            data['types_of_work'].append(i)
            data['desired_salary'].append(data[i])

    bot.send_message(callback.message.chat.id, 'Все данные получены, сейчас начнёться поиск', parse_mode='html')
    main(callback)
    bot.send_message(callback.message.chat.id, 'Поиск окончен\n<code>/start</code> для нового запроса', parse_mode='html')
    del session[callback.from_user.id]

TYPES_OF_YEARS_OF_EXPERIENCE = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
MINIMUM_YEARS_OF_EXPERIENCE = [0, 1, 3]
TYPES_OF_WORK = ['MONTH', 'SHIFT', 'HOUR', 'FLY_IN_FLY_OUT', 'SERVICE']

def main(callback):
    data = session[callback.from_user.id]

    for i in range(len(MINIMUM_YEARS_OF_EXPERIENCE)):
        if data['years_of_experience'] >= MINIMUM_YEARS_OF_EXPERIENCE[i]:
            for j in range(len(data['types_of_work'])):
                res = get(data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[i], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
                for vacancy in res:
                    #print(vacancy)
                    bot.send_message(callback.message.chat.id, vacancy, parse_mode='html')

    if data['years_of_experience'] >= 6:
        for j in range(len(data['types_of_work'])):
            res = get(data['desired_job'], data['desired_city'], TYPES_OF_YEARS_OF_EXPERIENCE[-1], TYPES_OF_WORK[data['types_of_work'][j]], data['desired_salary'][j], data['without_salary'])
            for vacancy in res:
                #print(vacancy)
                bot.send_message(callback.message.chat.id, vacancy, parse_mode='html')

bot.infinity_polling()