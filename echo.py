import json
import requests
import time
import urllib
import schedule

TOKEN = "429105357:AAHs2gkeSxYljcm8UkKRoM9lmDyJ7DPqj6g"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
CHAT_ID_K = "108123177"
CHAT_ID_A = ""
ERROR_MESSAGE = "Please enter something correct"

MYPILL_DATA = [{"time": "9:30", "message": "Get pill 200"},
               {"time": "21:30", "message": "Get pill 400"},
               {"time": "22:30", "message": "Get pill  one more 400"}]

for item in MYPILL_DATA:
    mytime = item["time"]
    mymsg = item["message"]
    print(mymsg + mytime)

#llll = len(MYPILL_DATA)
#pill0time = MYPILL_DATA[0]["time"]
#pill0msg = MYPILL_DATA[0]["message"]
#pill1time = MYPILL_DATA[1]["time"]

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
    return (text, chat_id)


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

def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def parse_message(updates):  #a copy of echo_all
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)
    return


def send_reminder():
    #copied send_message
    url = URL + "sendMessage?text={}&chat_id={}".format("Take a pill!", CHAT_ID_K)
    send_http_get_req(url)

def remind_me():
    schedule.every(1).minutes.do(send_reminder)


def set_schedule():
    schedule.every().day.at("23:26").do(remind_me)
    return


def main():
    last_update_id = None
    #get bot info to test bot status.
    #schedule.every(10).minutes.do(send_reminder)
    set_schedule()
    bot_inf_resp = get_bot_information()
    respOk = bot_inf_resp["ok"]
    if respOk:
        botIsOk = bot_inf_resp["result"]["is_bot"]
        if botIsOk:
            while True:
                schedule.run_pending()

                updates = get_updates(last_update_id)
                if len(updates["result"]) > 0:
                    last_update_id = get_last_update_id(updates) + 1
                    echo_all(updates)
                time.sleep(0.5)
        else:
            print("bot is not ok")
    else:
        print("bad response")

if __name__ == '__main__':
    main()


    #commands: /help, /add, /delete, /update, /view