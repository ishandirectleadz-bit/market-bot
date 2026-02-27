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

import time
import requests

def check_nifty():
    try:
        df = yf.download("^NSEI", period="1d", interval="5m")

        if df.empty:
            print("No data received. Waiting...")
            time.sleep(60)
            return

        df['EMA9'] = ta.trend.ema_indicator(df['Close'], 9)
        df['EMA21'] = ta.trend.ema_indicator(df['Close'], 21)

        latest = df.iloc[-1]

        if latest['EMA9'] > latest['EMA21']:
            message = "NIFTY CALL Signal\nEntry: Market Price\nSL: Below EMA21\nTarget: 20-40%"
        else:
            message = "NIFTY PUT Signal\nEntry: Market Price\nSL: Above EMA21\nTarget: 20-40%"

        send_telegram_message(message)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)

while True:
    check_nifty()
    time.sleep(300)
