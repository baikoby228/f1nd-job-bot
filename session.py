session = {}

def get_data(id: int):
    if not id in session:
        session[id] = {}

    return session[id]

def del_data(id: int):
    del session[id]