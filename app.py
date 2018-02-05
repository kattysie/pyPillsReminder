import time
import schedule
import json
import requests
import urllib
import sys
# from settings import Reminder
from settings import User
from settings import Reminder

TOKEN = "429105357:AAHs2gkeSxYljcm8UkKRoM9lmDyJ7DPqj6g"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def send_http_get_req(req_url):
    response = requests.get(req_url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = send_http_get_req(url)
    js = json.loads(content)
    return js


def get_bot_information():
    url = URL + "getMe"
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    send_http_get_req(url)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=2"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_forgot(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format("Take a pill! " + text, chat_id)
    send_http_get_req(url)


def send_reminder(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format("Take a pill! " + text, chat_id)
    send_http_get_req(url)
    schedule.every(5).minutes.do(send_forgot, text + " don't forget").tag('forgot')


class App:
    def __init__(self):
        self.reminder_list.append(Reminder("K", "10:20", "Pill", True))
        self.reminder_list.append(Reminder("K", "10:20", "Pill 1", True))
        self.reminder_list.append(Reminder("K", "21:45", "Pill 2", True))
        self.CHAT_ID_K = "108123177"
        self.CHAT_ID_A = "90979903"
        self.ERROR_MESSAGE = "I don't understand '%s' please enter something correct"
        self.reminder_list_K = [{"time": "11:15", "message": "Take a break", "repeat": 'False', "chatid": '108123177'},
                               {"time": "14:00", "message": "Have a lunch", "repeat": 'False', "chatid": '108123177'},
                               {"time": "17:10", "message": "Eat a snack", "repeat": 'False', "chatid": '108123177'}]  # add repeat True/False setting

    reminder_list = []

    def set_schedule(rem_list):
        for item in rem_list:
            my_time = item["time"]
            schedule.every().day.at(my_time).do(send_reminder, item["message"], item["chatid"]).tag('main_reminder')
        return

    def get_command(self, updates):
        text, chat_id = self.parse_message(updates)
        words =  text.lower().split()
        print(time.strftime("%H:%M:%S") + ' ' + str(chat_id) + ' ' + text)
        if words:
            cmd_text = words[0]
            if 'done' == cmd_text:
                send_message('Well done!', chat_id)
                schedule.clear('forgot')
            elif 'add' == cmd_text:
                send_message('Okay, so you want to add a reminder. Please enter it as in example: '
                             '"At 12:00 Do something important. Repeat: True"', chat_id)
                self.write_to_file(text, chat_id)  # need to add code to get the NEXT message
            elif 'delete' == cmd_text:
                pass
            elif 'view' == cmd_text:
                pass
            else:
                send_message(self.ERROR_MESSAGE % text, chat_id)
        else:
            print('Error No words in message')
        return {
            'wft': "how it worked before?"
        }.get(self.ERROR_MESSAGE)

    def write_to_file(self, text, chat_id):
        with open('schedule.txt', 'a') as s_file:
                s_file.write(time.strftime("%H:%M:%S") + ' ' + str(chat_id) + ' ' + text + '\n')

    def read_from_file(self):
        pass

    def view_details(self):
        for reminder in self.reminder_list:
            print(str(self.reminder_list.index(reminder))
                  + "%s's reminder:  At %s do %s. Repeat: %s"
                  % (self.user.name, self.time, self.comment, str(self.repeat)))

    def add_reminder(self, text, chat_id, updates):
        name = updates['result'][0]['message']['from']['username']
        words = text.lower().split()
        if 'at' == words[0] and 'do' == words[2] and 'repeat:' in words:
            r_time = words[1]
            i = words.index('repeat:')
            r_comment = words[3:i]
            repeat = bool(words[-1])
            reminder = Reminder(User(name, chat_id), r_time, r_comment, repeat)
            self.reminder_list.append(reminder)
            return 'Added!'
        else:
            return 'Wrong format!!!'


    def del_reminder(self):
        pass

    def parse_message(self, updates):
        for update in updates["result"]:
            try:
                text = (update["message"]["text"]).rstrip().lower()
                chat = update["message"]["chat"]["id"]
            except Exception as e:
                print(e)
        return text, chat

    # commands: /help, /update

    def run(self):
        print("Run...")
        last_update_id = None
        #get bot info to test bot status
        App.set_schedule(self.reminder_list_K)
        bot_inf_resp = get_bot_information()
        respOk = bot_inf_resp["ok"]
        if respOk:
            bot_is_ok = bot_inf_resp['result']["is_bot"]
            if bot_is_ok:
                print("Bot info received")
                while True:
                    try:
                        schedule.run_pending()
                        updates = get_updates(last_update_id)
                        if 'result' in updates and updates['result']:
                            last_update_id = get_last_update_id(updates) + 1
                            self.get_command(updates)
                    except:
                        print("Unexpected except")
                        raise

                    sys.stdout.flush()
                    time.sleep(0.5)
            else:
                print("bot is not ok")
        else:
            print("bad response")



#CREATE MAIN CLASS AND RUN
app = App()
app.run()
