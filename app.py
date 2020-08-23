import requests, sys, time, random, webbrowser, json, base64
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import parallel_coordinates, table

from flask import Flask, request, abort, render_template

from io import BytesIO

# 全域變數
app = Flask(__name__)

# Pandas 設定
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 函式庫
def GetCandle(pair):
    try:
        data = requests.get(f'https://ftx.com/api/markets/{pair}/candles?resolution=3600&limit=500').json()['result']
    except Exception as e:
        print ('Error! promblem is {}'.format(e.args[0]))
    df = pd.DataFrame(data)
    return df

def GetFundingRate(pair):
    try:
        data = requests.get(f'https://ftx.com/api/funding_rates?future={pair}').json()['result']
    except Exception as e:
        print ('Error! promblem is {}'.format(e.args[0]))
    df = pd.DataFrame(data)
    return df

def GetNextFundingRate(pair):
    try:
        data = requests.get(f'https://ftx.com/api/futures/{pair}/stats').json()['result']['nextFundingRate']
    except Exception as e:
        print ('Error! promblem is {}'.format(e.args[0]))
    return data * 100


def GetPrice(pair):
    try:
        data = requests.get(f'https://ftx.com/api/futures/{pair}').json()['result']['last']
    except Exception as e:
        print ('Error! promblem is {}'.format(e.args[0]))
    return data

# Math Tools
def Decimals(num: float, digit):
    return format(num, f'.{digit}f')

@app.route("/")
def home():
    # 資料
    PAXG = GetCandle('PAXG-PERP')
    XAUT = GetCandle('XAUT-PERP')
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    PAXG.close.plot(label = 'PAXG Price')
    XAUT.close.plot(label = 'PAXG Price')
    plt.legend()
    PAXG_PRICE   = GetPrice('PAXG-PERP')
    XAUT_PRICE   = GetPrice('XAUT-PERP')
    PREMIUM      = PAXG_PRICE - XAUT_PRICE
    PREMIUM_RATE = Decimals(PAXG_PRICE / XAUT_PRICE, 2)
    PAXG_RATE    = Decimals(GetNextFundingRate('PAXG-PERP'), 4)
    XAUT_RATE    = Decimals(GetNextFundingRate('XAUT-PERP'), 4)
    RATE_GAP     = Decimals(float(PAXG_RATE) - float(XAUT_RATE), 4)

    # 圖片處理
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    imd = "data:image/png;base64," + data
    print(data)
    
    # 網頁
    plt.close()
    return render_template('home.html',  PAXG = PAXG_PRICE, XAUT = XAUT_PRICE, premium = PREMIUM, premium_rate = PREMIUM_RATE, PAXG_RATE = PAXG_RATE, XAUT_RATE = XAUT_RATE, rate_gap = RATE_GAP, img = imd)

# main
if __name__ == "__main__":
    app.run()