class User:
    def __init__(self, name, chat_id):
        self.name = name
        self.chat_id = chat_id


class Reminder:
    def __init__(self, user, time, comment, repeat):
        self.user = user
        self.time = time
        self.comment = comment
        self.repeat = repeat




