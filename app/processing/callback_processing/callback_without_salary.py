import telebot

from dotenv import load_dotenv
import os

from ...user_session import get_user
from ...parser import iterate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_callback_without_salary(callback) -> None:
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    user = get_user(user_id)

    user.without_salary = callback.data == 'Yes'

    iterate(user_id, chat_id)