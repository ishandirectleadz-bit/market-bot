import yfinance as yf
import pandas as pd
import ta
import requests
import time

import os
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=payload)

def check_nifty():
    df = yf.download("^NSEI", interval="5m", period="1d")
    df['EMA9'] = ta.trend.ema_indicator(df['Close'], 9)
    df['EMA21'] = ta.trend.ema_indicator(df['Close'], 21)
    df['RSI'] = ta.momentum.rsi(df['Close'], 5)

    latest = df.iloc[-1]

    if latest['Close'] > latest['EMA9'] and latest['EMA9'] > latest['EMA21'] and latest['RSI'] > 60:
        send_message("🟢 NIFTY CALL Signal Detected (Conservative Model)")

while True:
    check_nifty()
    time.sleep(300)
