
from settings import Reminder


class App:
    def __init__(self):
        self.reminder_list.append( Reminder("10:20", "Pill", True) )
        self.reminder_list.append( Reminder("10:20", "Pill 1", True) )
        self.reminder_list.append( Reminder("21:45", "Pill 2", True) )
        self.reminder_list.append( Reminder("10:50", "Pill 4", True) )
        self.reminder_list.append( Reminder("20:20", "Pill 4238", True) )

    def run(self):
        for i in self.reminder_list:
            print(i.comment)

        while True:
            pass

    reminder_list = []
