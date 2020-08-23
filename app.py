import requests, sys, time, random, webbrowser, json, base64
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import parallel_coordinates, table

from flask import Flask, request, abort

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

def GetPrice(pair):
    try:
        data = requests.get(f'https://ftx.com/api/futures/{pair}').json()['result']['last']
    except Exception as e:
        print ('Error! promblem is {}'.format(e.args[0]))
    return data

@app.route("/")
def home():
    # 資料
    PAXG = GetCandle('PAXG-PERP')
    XAUT = GetCandle('XAUT-PERP')
    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    PAXG.close.plot(label = 'PAXG Price')
    XAUT.close.plot(label = 'PAXG Price')
    plt.legend()
    # PAXG_PRICE = GetPrice('PAXG-PERP')
    # XAUT_PRICE = GetPrice('XAUT-PERP')

    # 圖片處理
    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()
    print(data)
    
    # 網頁
    html = '''
    <!DOCTYPE html>

    <html lang="zh-tw">

        <head>

            <meta content="text/html; charset=utf-8" http-equiv="content-type">

            <title>FTX PAXG-XAUT 費率時實更新表</title>

            <meta content="FTX PAXG-XAUT 費率時實更新表" name="FTX PAXG-XAUT 費率時實更新表">
            <meta content="HTML>

            <meta name="author" content="FTX PAXG-XAUT 費率時實更新表">

            <link href="https://hyip.tw/Quantize/style.css" rel="stylesheet" type="text/css" />

        </head>

        <body>

            <div id="page">

            <h1 align="center"><br>FTX PAXG-XAUT 費率時實更新表</h1>

            <hr size=1></hr>

            <h3 align="left">
            一、<a href="#價格圖">價格圖</a><br>
            </h3>

            <h1 align="center" id="價格圖"><br>PAXG-XAUT 現價四小時圖</h1>

            <hr size=1></hr>

            <img src="data:image/png;base64,{}" />

            </div>
        
        </body>

    </html>
    '''
    plt.close()
    return html.format(data)

# main
if __name__ == "__main__":
    app.run()