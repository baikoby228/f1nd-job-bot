import telebot

from dotenv import load_dotenv
import os

from input_processing import input_processing
from command_processing import (command_start,
                                command_help,
                                command_job,
                                command_language)
from callback_processing import (callback_language,
                                callback_salary,
                                callback_without_salary)

from global_constants import LANGUAGES_SHORT

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'info'])
def command_start_handler(message):
    command_start.processing(message)

@bot.message_handler(commands=['help'])
def command_help_handler(message):
    command_help.processing(message)

@bot.message_handler(commands=['job'])
def command_job_handler(message):
    command_job.processing(message)

@bot.message_handler(commands=['language'])
def command_language_handler(message):
    command_language.processing(message)

@bot.callback_query_handler(func=lambda callback: callback.data in LANGUAGES_SHORT)
def callback_language_handler(callback):
    callback_language.processing(callback)

@bot.callback_query_handler(func=lambda callback: callback.data == 'finished' or '0' <= callback.data <= '4')
def callback_salary_handler(callback):
    callback_salary.processing(callback)

@bot.callback_query_handler(func=lambda callback: callback.data in ['Yes', 'No'])
def callback_without_salary_handler(callback):
    callback_without_salary.processing(callback)

@bot.message_handler(content_types=['text'])
def input_text(message):
    input_processing(message)

bot.infinity_polling()