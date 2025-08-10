import user_language_db

class UserData:
    step = -1

    desired_job: str
    desired_city: str
    years_of_experience: str

    cur_type: int
    desired_types: list
    desired_types_of_work: list
    desired_salary: list

    without_salary: bool

    def __init__(self, id: int):
        self.id = id

        self.language = user_language_db.get_language(self.id)
        if not self.language:
            self.language = 'ru'
            self.set_language('ru')

    def set_language(self, new_language: str):
        self.language = new_language
        user_language_db.set_language(self.id, new_language)

    def get_language(self):
        return user_language_db.get_language(self.id)