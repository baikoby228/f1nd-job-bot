import telebot

from dotenv import load_dotenv
import os

from session import get_data
from user_step import start_user_step

from steps import processing_step

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    data = get_data(user_id)

    start_user_step(user_id)
    for x in range(5):
        data[x] = -1

    processing_step(user_id, chat_id, 0)