import telebot
from telebot import types

from dotenv import load_dotenv
import os

from user_language import get_user_language

from translate import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

LANGUAGES_LONG = ['Русский', 'Английский', 'Белорусский']
LANGUAGES_SHORT = ['ru', 'en', 'be']

def processing(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    cur_language = get_user_language(user_id)

    markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(3):
        b = types.InlineKeyboardButton(translate(LANGUAGES_LONG[i], 'ru', cur_language), callback_data=LANGUAGES_SHORT[i])
        markup.add(b)

    bot.send_message(chat_id, translate('Выберите нужный язык', 'ru', cur_language), parse_mode='html', reply_markup=markup)