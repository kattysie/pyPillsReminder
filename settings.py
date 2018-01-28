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

    def view_details(self):
        print('At %s do %s. Repeat: %s' % (self.time, self.comment, str(self.repeat)))

    def add_reminder(self):
        pass

    def del_reminder(self):
        pass

    # time = ""
    # comment = ""
    # repeat = False
    # user = User("Andrey", 34935794)

# commands: /help, /update




