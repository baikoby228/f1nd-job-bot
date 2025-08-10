import telebot
from telebot import types

from dotenv import load_dotenv
import os

from ...user_session import get_user
from utils import translate
from config import LANGUAGES_LONG, LANGUAGES_SHORT

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_command_language(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = get_user(user_id)
    cur_language = user.get_language()

    markup = types.InlineKeyboardMarkup(row_width=3)
    for i in range(3):
        b = types.InlineKeyboardButton(translate(LANGUAGES_LONG[i], 'ru', cur_language), callback_data=LANGUAGES_SHORT[i])
        markup.add(b)

    bot.send_message(chat_id, translate('Выберите нужный язык', 'ru', cur_language), parse_mode='html', reply_markup=markup)