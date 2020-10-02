import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from FTX.client import Client

from flask import Flask, request, abort, render_template

from pandas.plotting import parallel_coordinates, table

# Pandas 設定
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth',100)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

client = Client('', '')
print (pd.DataFrame(client.get_public_all_perpetual_futures()).to_html())