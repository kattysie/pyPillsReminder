import json
import requests
import time
import urllib
import schedule
from settings import Reminder


TOKEN = "429105357:AAHs2gkeSxYljcm8UkKRoM9lmDyJ7DPqj6g"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
CHAT_ID_K = "108123177"
CHAT_ID_A = "90979903"
ERROR_MESSAGE = "I don't understand you, please enter something correct"

reminder_list_A = [{"time": "09:00", "message": "Take 200 pill"},
                   {"time": "21:00", "message": "Take 400 pill"}]


reminder_list_K = [{"time": "11:15", "message": "Take a break", "repeat": 'False'},
                   {"time": "14:00", "message": "Have a lunch", "repeat": 'False'},
                   {"time": "17:00", "message": "Eat a snack", "repeat": 'False'}]  # add repeat True/False setting


def set_schedule(rem_list):
    for item in rem_list:
        my_time = item["time"]
        schedule.every().day.at(my_time).do(send_reminder, item["message"]).tag('main_reminder')
    return


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


def parse_message(updates):
    for update in updates["result"]:
        try:
            text = (update["message"]["text"]).rstrip()
            chat = update["message"]["chat"]["id"]
            if text == 'done':
                send_message('Well done!', chat)
                schedule.clear('forgot')
            # elif text == 'add':
            #     add_new_reminder(text)
            else:
                send_message(get_command(text), chat)
        except Exception as e:
            print(e)
    return


def get_command(x):
    return{
        'add': "add a reminder in format: add 'time', 'comment'",
        'delete': "remove a reminder",
        'view': "get the list of reminders"
    }.get(x, ERROR_MESSAGE)


def send_forgot(text):
    url = URL + "sendMessage?text={}&chat_id={}".format("Take a pill! " + text, CHAT_ID_K)
    send_http_get_req(url)


def send_reminder(text):
    url = URL + "sendMessage?text={}&chat_id={}".format("Take a pill! " + text, CHAT_ID_K)
    send_http_get_req(url)
    schedule.every(5).minutes.do(send_forgot, text + " don't forget").tag('forgot')


# def remind_me():
#     #schedule.every(1).minutes.do(send_reminder)
#     schedule.every(10).seconds.do(check_reminder).tag('forgot')
#     # while not seen:
#     #     schedule.run_pending()
#     return


def main():
    a = Reminder('aaa', 'aaa', False)
    a.view_details()

    last_update_id = None
    # get bot info to test bot status
    set_schedule(reminder_list_K)
    bot_inf_resp = get_bot_information()
    respOk = bot_inf_resp["ok"]
    if respOk:
        bot_is_ok = bot_inf_resp['result']["is_bot"]
        if bot_is_ok:
            while True:
                schedule.run_pending()

                updates = get_updates(last_update_id)
                if updates['result']:
                    last_update_id = get_last_update_id(updates) + 1
                    parse_message(updates)
                time.sleep(0.5)
        else:
            print("bot is not ok")
    else:
        print("bad response")

if __name__ == '__main__':
    main()
