import requests
import sys
sys.path.append('.')
from modules.yf import GetSPX
from modules.level import GetLevel
from modules.timer import RepeatedTimer
from time import sleep
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv
import datetime

weekday = datetime.date.today().weekday()

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

def Alert(message):
    payload = {
        "username": "",
        "content": message
    }

    requests.post(WEBHOOK_URL, json=payload)

range = 55
if weekday == 1: range = 10

def CheckCreditSpreadOP():
    price = GetSPX()
    price = GetLevel(price)
    sellStrike = price - range
    buyStrike = sellStrike - 5
    message = "SPY: " + str(price) + "\n"
    message += f"Sell {sellStrike} PUT Buy {buyStrike} PUT \n"
    Alert(message)

print ("starting...")

starttime = time.time()
while True:
    print("tick")
    CheckCreditSpreadOP()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))