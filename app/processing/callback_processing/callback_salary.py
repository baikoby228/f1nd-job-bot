import telebot
from telebot import types

from dotenv import load_dotenv
import os

from ...user_session import get_user
from utils import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_callback_salary(callback) -> None:
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    user = get_user(user_id)
    cur_language = user.get_language()

    if callback.data == 'finished':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button_yes = types.InlineKeyboardButton(translate('Да', 'ru', cur_language), callback_data='Yes')
        button_no = types.InlineKeyboardButton(translate('Нет', 'ru', cur_language), callback_data='No')
        markup.add(button_yes, button_no)

        bot.send_message(chat_id, translate('Показывать объявления без указанной зарплаты?', 'ru', cur_language), parse_mode='html', reply_markup=markup)
        user.step = -1
        return

    user.cur_type = int(callback.data)
    bot.send_message(chat_id, f'{translate('Введите минимальную зарплату в', 'ru', cur_language)} BYN', parse_mode='html')
    user.step = 4