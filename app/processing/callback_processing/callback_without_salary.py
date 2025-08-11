import telebot

from dotenv import load_dotenv
import os

from ...user_session import get_user, del_user
from ...parser import iterate
from utils import translate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_callback_without_salary(callback) -> None:
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    user = get_user(user_id)
    cur_language = user.get_language()

    user.without_salary = callback.data == 'Yes'

    iterate(user_id, chat_id)

    text = (
        f'{translate('Поиск окончен', 'ru', cur_language)}\n'
        f'<code>/job</code> {translate('для нового запроса', 'ru', cur_language).lower()}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')

    del_user(user_id)