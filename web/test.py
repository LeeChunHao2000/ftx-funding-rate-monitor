import requests
import pandas as pd

data = requests.get('https://ftx.com/api/funding_rates?future=PAXG-PERP').json()['result']
df = pd.DataFrame(data)
df = df.set_index('time')
df = df.drop(columns=['future'])
x = float(df.sum())
print (x)