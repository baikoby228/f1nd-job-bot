import telebot

from dotenv import load_dotenv
import os

from ...user_session import get_user
from utils import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_command_help(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = get_user(user_id)
    cur_language = user.get_language()

    text = (
        f'<code>/info</code> {translate(' я расскажу о себе', 'ru', cur_language).lower()}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', cur_language).lower()}\n'
        f'<code>/language</code> {translate(' для смены языка', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')