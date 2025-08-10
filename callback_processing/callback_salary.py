import telebot
from telebot import types

from dotenv import load_dotenv
import os

from session import get_data
from user_language import get_user_language
from user_step import set_user_step

from translate import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = get_data(user_id)
    cur_language = get_user_language(user_id)

    if callback.data == 'finished':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button_yes = types.InlineKeyboardButton(translate('Да', 'ru', cur_language), callback_data='Yes')
        button_no = types.InlineKeyboardButton(translate('Нет', 'ru', cur_language), callback_data='No')
        markup.add(button_yes, button_no)

        bot.send_message(chat_id, translate('Показывать объявления без указанной зарплаты?', 'ru', cur_language), parse_mode='html', reply_markup=markup)
        set_user_step(user_id, -1)
        return

    data['cur_type'] = int(callback.data)
    bot.send_message(chat_id, f'{translate('Введите минимальную зарплату в', 'ru', cur_language)} BYN', parse_mode='html')
    set_user_step(user_id, 4)