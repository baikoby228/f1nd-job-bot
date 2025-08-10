import sqlite3

def create_db():
    db = sqlite3.connect('user_data_base.db')
    c = db.cursor()

    c.execute("""CREATE TABLE user_language(
        id INTEGER PRIMARY KEY,
        language TEXT
    )""")

    db.commit()
    db.close()

def set_language(id: int, new_language: str):
    db = sqlite3.connect('user_data_base.db')
    c = db.cursor()

    c.execute("INSERT OR REPLACE INTO user_language VALUES (?, ?)", (id, new_language))

    db.commit()
    db.close()


def get_language(id: int):
    db = sqlite3.connect('user_data_base.db')
    c = db.cursor()

    c.execute("SELECT language FROM user_language WHERE id = ?", (id,))
    res = c.fetchone()

    db.close()

    return res[0] if res else None

'''
if __name__ == '__main__':
    create_db()
'''