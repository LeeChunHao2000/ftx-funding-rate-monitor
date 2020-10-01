import requests, time, json, base64
import pandas as pd
import matplotlib.pyplot as plt

from io import BytesIO

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
    return 'home'

@app.route("/<coin>")
def perpetual(coin):
    return 'Perpetual: ' + coin

# main
if __name__ == "__main__":
    app.run()