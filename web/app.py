import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from FTX.client import Client

from flask import Flask, request, abort, render_template

from pandas.plotting import parallel_coordinates, table

# 全域變數
app = Flask(__name__)

# Pandas 設定
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

@app.route("/")
def home():
    client = Client('', '')
    df = pd.DataFrame(client.get_public_all_perpetual_futures())
    df = pd.DataFrame(df, columns=['name', 'underlying', 'underlyingDescription'])
    df.columns = ['Name', 'Symbol', 'Full name']
    return render_template('home.html', tables=[df.to_html()])

@app.route("/<coin>")
def perpetual(coin):

    quarter = coin.upper() + '-1225'
    coin    = coin.upper() + '-PERP'

    client = Client('', '')

    currentPrice           = client.get_public_single_future(coin)['last']
    quarterPrice           = client.get_public_single_future(quarter)['last']
    premiumPrice           = round(quarterPrice - currentPrice, 2)
    premiumPriceRate       = round((premiumPrice / currentPrice) * 100, 2)

    nextFundingRate        = round(client.get_public_future_stats(coin)['nextFundingRate'] * 100, 4)
    lastFundingRate        = round(client.get_public_single_funding_rates(coin)[0]['rate'] * 100, 4)

    currentKLine           = pd.DataFrame(client.get_public_k_line(coin, 3600, 500)).close
    quarterKLine           = pd.DataFrame(client.get_public_k_line(quarter, 3600, 500)).close

    fundingRateHistory     = pd.DataFrame(client.get_public_single_funding_rates(coin)).rate * 100

    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    currentKLine.plot(label = coin + ' Price')
    quarterKLine.plot(label = quarter + ' Price')
    plt.legend()
    plt.savefig(f'/app/static/img/{coin}.png')
    plt.cla()

    plt.rcParams['figure.figsize'] = (8.0, 4.0)
    fundingRateHistory.plot(label = coin + ' Rate')
    plt.legend()
    plt.savefig(f'/app/static/img/{coin}-Rate.png')
    plt.cla()

    return render_template('coin.html', coin = coin, currentPrice = currentPrice, quarterPrice = quarterPrice, premiumPrice = premiumPrice, premiumPriceRate = premiumPriceRate, nextFundingRate = nextFundingRate, lastFundingRate = lastFundingRate)

# main
if __name__ == "__main__":
    app.run()