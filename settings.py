class Reminder:
    def __init__(self, time, comment, repeat):
        self.time = time
        self.comment = comment
        self.repeat = repeat

    def view_details(self):
        print('At %s do %s. Repeat: %s' % (self.time, self.comment, str(self.repeat)))

    def add_reminder(self):
        pass

    def del_reminder(self):
        pass

# commands: /help, /update



