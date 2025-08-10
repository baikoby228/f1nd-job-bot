from ..user_session import get_user
from .steps import processing_step

def input_processing(message) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id

    user = get_user(user_id)
    current_step = user.step

    if current_step != -1:
        processing_step(user_id, chat_id, message.text)