import requests
import json
from inputs import TELEGRAM_TOKEN

def send_telegram(msg, chatid):
    if chatid != 'none' and chatid:
        BOT_SEND_MSG_URL = 'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&disable_notification=None&text={msg}'
        url = BOT_SEND_MSG_URL.format(token=TELEGRAM_TOKEN, chat_id=chatid, msg=msg)
        try:
            r = requests.get(url)
            result = json.loads(r.text)
            print (result)
            return result.get('ok', False)
        except Exception as e:
            print (e)            

# Python 2 not support
# def alert(msg, chatid):
#     bot.send_message(chat_id=chatid, text=msg, parse_mode=ParseMode.MARKDOWN_V2)
