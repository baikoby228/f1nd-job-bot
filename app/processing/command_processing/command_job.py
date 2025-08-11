import telebot

from dotenv import load_dotenv
import os

from ...user_session import create_user, del_user
from ..steps import processing_step

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing_command_job(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = create_user(user_id)

    user.desired_types = [-1] * 5
    user.step = 0

    processing_step(user_id, chat_id)