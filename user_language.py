user_language = {}

def get_user_language(id: int) -> str:
    if not id in user_language:
        user_language[id] = 'ru'

    return user_language[id]

def update_user_language(id: int, new_language: str):
    user_language[id] = new_language