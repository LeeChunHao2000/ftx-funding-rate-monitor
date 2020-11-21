import plotly
import requests
import pandas as pd
import cufflinks as cf

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

from FTX.client import Client

from flask import Flask, request, abort, render_template

# from pandas.plotting import parallel_coordinates, table

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# 全域變數
app = Flask(__name__)
client = Client('', '')
cf.set_config_file(offline=True)

def get_k_line(symbol, resolution, start='', end='', limit=500):
    payload = {
        'resolution': resolution,
        'limit': limit
    }

    if start:
        payload.update({
            'start_time': start
        })

    if end:
        payload.update({
            'end_time': end
        })

    data = requests.get(f'https://ftx.com/api/markets/{symbol}/candles', params=payload).json()['result']
    date = [i['startTime'] for i in data]
    line = [i['close'] for i in data]
    df = pd.DataFrame(date, columns=['datetime'])
    df = df.set_index('datetime')
    df[symbol] = line

    return df

def get_funding_rate(symbol):
    data = requests.get(f'https://ftx.com/api/funding_rates?future={symbol}').json()['result']
    date = [i['time'] for i in data]
    rate = [i['rate'] * 100 for i in data]
    df = pd.DataFrame(date, columns=['datetime'])
    df = df.set_index('datetime')
    df['rate'] = rate

    return df

@app.route("/")
def home():

    df = pd.DataFrame(client.get_public_all_perpetual_futures())
    df = pd.DataFrame(df, columns=['name', 'underlying', 'underlyingDescription'])
    df.columns = ['Name', 'Symbol', 'Full name']

    rateSum = []
    for coin in df.Name:
        data = pd.DataFrame(client.get_public_single_funding_rates(coin))
        sum = float(data.rate.sum())
        rateSum.append(round(abs(sum) * 100, 4))
    
    df['Rates (500 hrs)'] = rateSum
    df.sort_values("Rates (500 hrs)", inplace=True, ascending=False)

    return render_template('home.html', tables=[df.to_html()])

@app.route("/<coin>")
def perpetual(coin):

    quarter = coin.upper() + '-1225'
    coin    = coin.upper() + '-PERP'

    currentPrice           = client.get_public_single_future(coin)['last']
    quarterPrice           = client.get_public_single_future(quarter)['last']

    premiumPrice           = round(quarterPrice - currentPrice, 2)
    premiumPriceRate       = round((premiumPrice / currentPrice) * 100, 2)

    nextFundingRate        = round(client.get_public_future_stats(coin)['nextFundingRate'] * 100, 4)
    lastFundingRate        = round(client.get_public_single_funding_rates(coin)[0]['rate'] * 100, 4)

    currentKLine           = get_k_line(coin, 3600)
    quarterKLine           = get_k_line(quarter, 3600)

    df = pd.concat([currentKLine, quarterKLine], axis=1)
    df.index = pd.to_datetime(df.index)
    fig = df.iplot(asFigure=True)
    plotly.offline.plot(fig, filename=f"/app/templates/{coin}_premium.html")


    rate = get_funding_rate(coin)
    rate.index = pd.to_datetime(rate.index)
    fig = rate.iplot(asFigure=True)
    plotly.offline.plot(fig, filename=f"/app/templates/{coin}_rate.html")

    return render_template('coin.html', coin = coin, currentPrice = currentPrice, quarterPrice = quarterPrice, premiumPrice = premiumPrice, premiumPriceRate = premiumPriceRate, nextFundingRate = nextFundingRate, lastFundingRate = lastFundingRate)

# main
if __name__ == "__main__":
    app.run()