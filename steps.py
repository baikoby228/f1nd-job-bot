import telebot
from telebot import types

from dotenv import load_dotenv
import os

from session import get_user
from find_number import find_number
from translate import translate, translate_city, translate_job

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

TYPES_OF_WORK_RU = ['За месяц', 'За смену', 'За час', 'За вахту', 'За услугу']

def processing_step(user_id, chat_id, text: str = '-1') -> None:
    user = get_user(user_id)
    cur_language = user.get_language()

    match user.step:
        case 0:
            bot.send_message(chat_id, translate('Введите профессию', 'ru', cur_language), parse_mode='html')
            user.step += 1
        case 1:
            user.desired_job = translate_job(text, cur_language, 'ru')
            bot.send_message(chat_id, translate('Введите название города', 'ru', cur_language), parse_mode='html')
            user.step += 1
        case 2:
            user.desired_city = translate_city(text)
            bot.send_message(chat_id, translate('Введите количество лет опыта работы в этой профессии', 'ru', cur_language), parse_mode='html')
            user.step += 1
        case 3:
            if text != '-1':
                user.years_of_experience = int(find_number(text))

            is_ready = False
            markup = types.InlineKeyboardMarkup()
            for i in range(5):
                button = types.InlineKeyboardButton(f'{translate(TYPES_OF_WORK_RU[i], 'ru', cur_language)}: {'-' if user.desired_types[i] < 0 else user.desired_types[i]}', callback_data=str(i))
                markup.add(button)
                is_ready |= user.desired_types[i] >= 0

            finish_text = ''
            if is_ready:
                button = types.InlineKeyboardButton(translate('Готово!', 'ru', cur_language), callback_data='finished')
                markup.add(button)
                finish_text = '. Если введённые данные верны нажмите Готово!'

            bot.send_message(chat_id, translate(f'Выберите типы оплаты {finish_text}', 'ru', cur_language), parse_mode='html', reply_markup=markup)

            user.step = -1
        case 4:
            user.desired_types[int(user.cur_type)] = int(find_number(text))
            user.step = 3
            processing_step(user_id, chat_id)