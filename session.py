from user_data import UserData

session = {}

def create_user(id: int):
    if not id in session:
        session[id] = UserData(id)

def get_user(id: int):
    if not id in session:
        create_user(id)

    return session[id]

def del_user(id: int):
    del session[id]