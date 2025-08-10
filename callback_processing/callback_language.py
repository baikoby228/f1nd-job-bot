import telebot

from dotenv import load_dotenv
import os

from user_language import get_user_language, update_user_language

from translate import translate

from global_constants import LANGUAGES_LONG, LANGUAGES_SHORT

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing(callback):
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