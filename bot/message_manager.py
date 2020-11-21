import time
import requests
import os
from . import settings

OK_CODES = (200, 201, 202, 203, 204)

def get_updates(token):
    get_updates_url = f"{settings.root_address}{token}/getUpdates"
    offset = None
    params = {'timeout': 100, 'offset': offset}
    res = requests.get(get_updates_url, data=params)
    updates = res.json()["result"]
    if len(updates) >= 4:
        offset = updates[-1]["update_id"]
    return updates

def send_message(chat_id,  message=""): 
    sendMessage = f"{settings.root_address}{settings.token}/sendMessage"
    requests.post(sendMessage, data={"text":message, "chat_id":chat_id})
    return True
    pass


def get_single_currency(currency_code:str):
    currency_url = f"https://www.nbrb.by/api/exrates/rates/{currency_code}?parammode=2"
    res = requests.get(currency_url)
    if res.status_code in OK_CODES:
        data = res.json()
        return data
    else:
        raise Exception(f"Response was return witth status {res.status_code}, check connection")

def prepare_currs(abrs:str):
    all_abrs = abrs.replace(" ", "").lower().split(",")
    extracted_currencies = []
    for abr in all_abrs:
        extracted_currencies.append(get_single_currency(abr))
    return extracted_currencies


def prepare_message(abrs:str):
    base_message = "Курс на сегодя по запрошенным валютам составляет:"
    raw_data = prepare_currs(abrs)
    template = "За {scale} {cur_abr} {rate} бел.руб \n"
    for currency_info in raw_data:
        curr_scale = currency_info["Cur_Scale"]
        curr_abr = currency_info["Cur_Abbreviation"] 
        rate = currency_info["Cur_OfficialRate"]
        base_message += "За {} {} {} бел.руб \n".format(curr_scale, curr_abr, rate) 
    return base_message

def process_message(message):
    message = message["message"]
    message_text = message["text"]
    chat_id = message["chat"]["id"]
    if "курсы:" in message_text:
        data = message_text[:6]
        mess = prepare_message(data)
        send_message(chat_id, mess)
    else:
        send_message(chat_id,  settings.WITHOUT_EMAIL_MESSAGE) 

def process_input_messages(messages):
    last_update_id = os.environ.get("LAST_UPDATE_ID")
    messages_count = len(messages)
    if messages_count >= 4:
        # log too many messaes!!!
        messages = messages[-4:]
    else:
        messages = messages[-messages_count:]
    if last_update_id:
        last_update_id = int(last_update_id)
    
        if last_update_id == messages[-1]["update_id"]:
            return True
        else:
            for message in messages:
                # не самый экономный способ. Раввернуть список
                if message["update_id"] > last_update_id:
                    process_message(message)
                    last_update_id = message["update_id"]
                    os.environ["LAST_UPDATE_ID"]= str(last_update_id)
            return True
    else:
        for message in messages:    
            process_message(message)
            last_update_id = message["update_id"]
            os.environ["LAST_UPDATE_ID"]= str(last_update_id)
            # Не очень экономео, лучше только один раз ласт апдейтменяь
        return True

def run_pooling(frequency:int, token:str):
    # frequency - колличество секунд ожидания
    while True:
        messages = get_updates(token)
        process_input_messages(messages)
        time.sleep(frequency)
