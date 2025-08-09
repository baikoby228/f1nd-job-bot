import telebot

from dotenv import load_dotenv
import os

from user_language import get_user_language

from translate import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    cur_language = get_user_language(user_id)

    text = (
        f'<code>/start</code> {translate(' я расскажу о себе', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', cur_language)}\n'
        f'<code>/language</code> {translate(' для смены языка', 'ru', cur_language)}'
    )
    bot.send_message(chat_id, text, parse_mode='html')