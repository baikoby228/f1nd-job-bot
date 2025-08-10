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
        f'{translate('Привет! Я дам все вакансии на', 'ru', cur_language)} rabota.by {translate('по заданным критериям', 'ru', cur_language).lower()}\n'
        f'<code>/job</code> {translate(' для поиска по критериям', 'ru', cur_language).lower()}\n'
        f'<code>/help</code> {translate(' для всех команд', 'ru', cur_language).lower()}'
    )
    bot.send_message(chat_id, text, parse_mode='html')