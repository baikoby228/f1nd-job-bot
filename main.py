import telebot

from dotenv import load_dotenv
import os

from app import (input_processing,
                 processing_command_start, processing_command_help, processing_command_job, processing_command_language,
                 processing_callback_language, processing_callback_salary, processing_callback_without_salary)
from config import LANGUAGES_SHORT

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'info'])
def command_start_handler(message):
    processing_command_start(message)

@bot.message_handler(commands=['help'])
def command_help_handler(message):
    processing_command_help(message)

@bot.message_handler(commands=['job'])  
def command_job_handler(message):
    processing_command_job(message)

@bot.message_handler(commands=['language'])
def command_language_handler(message):
    processing_command_language(message)

@bot.callback_query_handler(func=lambda callback: callback.data in LANGUAGES_SHORT)
def callback_language_handler(callback):
    processing_callback_language(callback)

@bot.callback_query_handler(func=lambda callback: callback.data == 'finished' or '0' <= callback.data <= '4')
def callback_salary_handler(callback):
    processing_callback_salary(callback)

@bot.callback_query_handler(func=lambda callback: callback.data in ['Yes', 'No'])
def callback_without_salary_handler(callback):
    processing_callback_without_salary(callback)

@bot.message_handler(content_types=['text'])
def input_text(message):
    input_processing(message)

bot.infinity_polling()