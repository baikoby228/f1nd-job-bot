import telebot

from dotenv import load_dotenv
import os

from session import get_data

from iterate import iterate

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

def processing(callback):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = get_data(user_id)

    data['without_salary'] = callback.data == 'Yes'

    data['types_of_work'] = []
    data['desired_salary'] = []
    for i in range(5):
        if i in data and data[i] >= 0:
            data['types_of_work'].append(i)
            data['desired_salary'].append(data[i])

    iterate(user_id, chat_id)