import requests
from os import getenv


TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = "https://api.telegram.org/bot"


def send_telegram(text: str, destination_id):
    url = TELEGRAM_API_URL + TELEGRAM_BOT_TOKEN + "/sendMessage"
    requests.post(url, data={
         "chat_id": destination_id,
         "text": text
          })


def send_me_report(report):
    my_id = "396361880"
    send_telegram(report, my_id)
