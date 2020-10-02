import requests
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from FTX.client import Client

from flask import Flask, request, abort, render_template

from pandas.plotting import parallel_coordinates, table

client = Client('', '')
print (pd.DataFrame(client.get_public_k_line('BTC-PERP', 900, 500)))
print ('=============================================================')
print (pd.DataFrame(client.get_public_k_line('ETH-1225', 900, 500)))