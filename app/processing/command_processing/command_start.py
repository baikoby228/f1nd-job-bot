import telebot

from dotenv import load_dotenv
import os

from ...user_session import create_user, del_user
from utils import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_command_start(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = create_user(user_id)
    cur_language = user.get_language()

    text = (
        f'{translate('Привет! Я дам все вакансии на', 'ru', cur_language)} rabota.by {translate('по заданным критериям', 'ru', cur_language).lower()}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', cur_language).lower()}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')

    del_user(user_id)