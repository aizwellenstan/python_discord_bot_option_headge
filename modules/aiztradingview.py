import json
from bs4 import BeautifulSoup
import sys
import pandas as pd
from user_agent import generate_user_agent
import requests
import urllib3
from lxml import html
import lxml
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SCANNER_URL = "https://scanner.tradingview.com/america/scan"
SCANNER_URL_JP = "https://scanner.tradingview.com/japan/scan"

def http_request_post(
    url, session=None, payload=None, data={}, parse=True, user_agent=generate_user_agent()
):
    data = json.dumps(data)
    if payload is None:
        payload = {}
    try:
        if session:
            content = session.post(
                url,
                params=payload,
                data=data,
                verify=False,
                headers={"User-Agent": user_agent},
            )
        else:
            content = requests.post(
                url,
                params=payload,
                data=data,
                verify=False,
                headers={"User-Agent": user_agent},
            )
        content.raise_for_status()  # Raise HTTPError for bad requests (4xx or 5xx)
        if parse:
            return html.fromstring(content.text), content.url
        else:
            return content.text, content.url
    except:
        print("time out")

def isLetter(inputStr):
    if "." in inputStr: return False
    return ''.join(c for c in inputStr if c.isalpha())

def GetChange():
    page_parsed = http_request_post(
        url=SCANNER_URL ,
        data= {
            "filter":[
                {"left":"name","operation":"nempty"},
                {"left":"type","operation":"equal","right":"fund"},
                {"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]},
            ], 
            "options":{"lang":"en"},
            "symbols":{"query":{"types":[]},"tickers":[]},"columns":["change"],"sort":{"sortBy":"average_volume_90d_calc","sortOrder":"desc"}
        },
        parse=True
    )
    data, url = page_parsed

    data = json.loads(data.text)
    data = data['data']

    attrDict = {}
    for d in data:
        symbol = d['s'].split(":")[1]
        if symbol == "DIA" or symbol == "SPY":
            change = d['d'][0]
            attrDict[symbol] = change
            
    return attrDict
    
def GetSPY():
    page_parsed = http_request_post(
        url=SCANNER_URL ,
        data= {
            "filter":[
                {"left":"name","operation":"nempty"},
                {"left":"type","operation":"equal","right":"fund"},
                {"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]},
            ], 
            "options":{"lang":"en"},
            "symbols":{"query":{"types":[]},"tickers":[]},"columns":["close"],"sort":{"sortBy":"average_volume_90d_calc","sortOrder":"desc"}
        },
        parse=True
    )
    data, url = page_parsed

    data = json.loads(data.text)
    data = data['data']

    attrDict = {}
    for d in data:
        symbol = d['s'].split(":")[1]
        if symbol == "SPY":
            last = d['d'][0]
            
    return last

def GetGap():
    page_parsed = http_request_post(
        url=SCANNER_URL ,
        data= {
            "filter":[
                {"left":"name","operation":"nempty"},
                {"left":"type","operation":"equal","right":"fund"},
                {"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]},
            ], 
            "options":{"lang":"en"},
            "symbols":{"query":{"types":[]},"tickers":[]},"columns":["gap"],"sort":{"sortBy":"average_volume_90d_calc","sortOrder":"desc"}
        },
        parse=True
    )
    data, url = page_parsed

    data = json.loads(data.text)
    data = data['data']

    attrDict = {}
    for d in data:
        symbol = d['s'].split(":")[1]
        if symbol == "DIA" or symbol == "SPY":
            gap = d['d'][0]
            attrDict[symbol] = gap
            
    return attrDict

def GetClose():
    page_parsed = http_request_post(
        url=SCANNER_URL ,
        data= {
            "filter":[
                {"left":"name","operation":"nempty"},
                {"left":"type","operation":"equal","right":"fund"},
                {"left":"exchange","operation":"in_range","right":["AMEX","NASDAQ","NYSE"]},
            ], 
            "options":{"lang":"en"},
            "symbols":{"query":{"types":[]},"tickers":[]},"columns":["close"],"sort":{"sortBy":"average_volume_90d_calc","sortOrder":"desc"}
        },
        parse=True
    )
    data, url = page_parsed

    data = json.loads(data.text)
    data = data['data']

    attrDict = {}
    for d in data:
        symbol = d['s'].split(":")[1]
        if symbol == "DIA" or symbol == "SPY":
            last = d['d'][0]
            attrDict[symbol] = last
            
    return attrDict