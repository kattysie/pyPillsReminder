import time
import schedule
from settings import Reminder
import chat
from settings import User
from settings import Reminder


CHAT_ID_K = "108123177"
CHAT_ID_A = "90979903"
ERROR_MESSAGE = "I don't understand you, please enter something correct"


reminder_list_A = [{"time": "09:00", "message": "Take 200 pill"},
                   {"time": "21:00", "message": "Take 400 pill"}]


reminder_list_K = [{"time": "11:15", "message": "Take a break", "repeat": 'False'},
                   {"time": "14:00", "message": "Have a lunch", "repeat": 'False'},
                   {"time": "17:10", "message": "Eat a snack", "repeat": 'False'}]  # add repeat True/False setting


class App:
    def __init__(self):
        self.reminder_list.append(Reminder("K", "10:20", "Pill", True))
        self.reminder_list.append(Reminder("K", "10:20", "Pill 1", True))
        self.reminder_list.append(Reminder("K", "21:45", "Pill 2", True))

    reminder_list = []

    def set_schedule(rem_list):
        for item in rem_list:
            my_time = item["time"]
            schedule.every().day.at(my_time).do(chat.send_reminder, item["message"]).tag('main_reminder')
        return

    def get_command(self):
        chat_id, text = chat.parse_message()
        if 'done' == text:
            chat.send_message('Well done!', chat)
            schedule.clear('forgot')
        elif 'add' == text:
            pass
        elif 'delete' == text:
            pass
        elif 'view' == text:
            pass
        else:
            chat.send_message(text, chat)  #not sure what it supposed to do
        return {
            'wft': "how it worked before?"
        }.get(ERROR_MESSAGE)

    def view_details(self):
        for reminder in self.reminder_list:
            print(str(self.reminder_list.index(reminder))
                  + "%s's reminder:  At %s do %s. Repeat: %s"
                  % (self.user.name, self.time, self.comment, str(self.repeat)))

    def add_reminder(self, user, time, comment, repeat):
        item = Reminder(User(user, CHAT_ID_K), time, comment, repeat)
        self.reminder_list.append(item)

    def del_reminder(self):
        pass

    # commands: /help, /update

    def run(self):
        for i in self.reminder_list:
            print(i.comment)

        while True:

            # last_update_id = None
            # get bot info to test bot status
            # set_schedule(reminder_list_K)
            # bot_inf_resp = get_bot_information()
            # respOk = bot_inf_resp["ok"]
            # if respOk:
            #     bot_is_ok = bot_inf_resp['result']["is_bot"]
            #     if bot_is_ok:
            #         while True:
            #             schedule.run_pending()
            #             updates = get_updates(last_update_id)
            #             if updates['result']:
            #                 last_update_id = get_last_update_id(updates) + 1
            #                 parse_message(updates)
            #             time.sleep(0.5)
            #     else:
            #         print("bot is not ok")
            # else:
            #     print("bad response")