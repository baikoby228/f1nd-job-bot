user_step = {}

def start_user_step(id: int):
    user_step[id] = 0

def get_user_step(id: int) -> int:
    if not id in user_step:
        return -1

    return user_step[id]

def set_next_user_step(id: int):
    user_step[id] += 1

def set_user_step(id: int, new_user_step: int):
    user_step[id] = new_user_step

def del_user_step(id: int):
    del user_step[id]