import requests
import sys
sys.path.append('.')
from modules.aiztradingview import GetGap, GetClose
from modules.timer import RepeatedTimer
from time import sleep
import time
import os
from os.path import join, dirname
from dotenv import load_dotenv

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

def CheckCloseHeadge():
    changeDict = GetChange()
    diaChange = changeDict["DIA"]
    spyChange = changeDict["SPY"]
    
    message = "diaChange: " + str(diaChange) + "\n" + "spyChange: " + str(spyChange)
    if diaChange >= spyChange:
        Alert(message)

def CheckGap():
    gapDict = GetGap()
    diaGap = gapDict["DIA"]
    spyGap = gapDict["SPY"]

    closeDict = GetClose()
    diaClose = closeDict["DIA"]
    spyClose = closeDict["SPY"]
    
    message = "diaClose: " + str(diaClose) +" diaGap: " + str(diaGap) + "\n" + "spyClose: " + str(spyClose) +" spyGap: " + str(spyGap)
    Alert(message)
    if diaGap < spyGap:
        Alert('DIAGap < SPYGap spread: '+str(spyGap-diaGap))

print ("starting...")
# rt = RepeatedTimer(1, CheckCloseHeadge) # it auto-starts, no need of rt.start()
# try:
#     sleep(5) # your long-running job goes here...
# finally:
#     rt.stop() # better in a try/finally block to make sure the program ends!

starttime = time.time()
while True:
    print("tick")
    CheckGap()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))