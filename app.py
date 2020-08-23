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

@app.route("/")
def home():
    html = '''
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title></title>
            <link href="style.css" rel="stylesheet" type="text/css" />
        </head>
        <body>
        
        </body>
    </html>
    '''
    return "賴田捕手第 20 天"

# main
if __name__ == "__main__":
    app.run()