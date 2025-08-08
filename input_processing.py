from steps import processing_step
from user_step import get_user_step

def input_processing(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    current_step = get_user_step(user_id)

    if current_step != -1:
        processing_step(user_id, chat_id, current_step, message.text)