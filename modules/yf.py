import yfinance as yf
import numpy as np

stockInfo = yf.Ticker("^SPX")
def GetSPX():
    hist = stockInfo.history(period="7d",interval = "1m",prepost = True)
    return hist.iloc[-1]['Close']