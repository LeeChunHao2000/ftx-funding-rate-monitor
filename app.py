import requests, sys, time, random, webbrowser, json
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import parallel_coordinates, table

from flask import Flask, request, abort

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
    html = '''
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title></title>
            <link href="https://www.hyip.tw/Aboutme/assets/css/main.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
        132
        </body>
    </html>
    '''
    return html

# main
if __name__ == "__main__":
    app.run()