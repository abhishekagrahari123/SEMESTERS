import pandas as pd
from datetime import datetime
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt

snx = pd.read_csv('bse/sensex.csv', usecols=[0, 4])
nifty = pd.read_csv('nse/nifty.csv', usecols=[0, 4])
bse = pd.read_csv('bse/bse.csv')
nse = pd.read_csv('nse/nse.csv')

snx['Date'] = pd.to_datetime(snx['Date'])
nifty['Date'] = pd.to_datetime(nifty['Date'])
bse['Date'] = pd.to_datetime(bse['Date'])
nse['Date'] = pd.to_datetime(nse['Date'])


def Index(Index, indexName):
    filt = Index['Date'] >= '2018-12-1'
    Index_last_month = Index.loc[filt]
    Returns = Index_last_month['Close'].pct_change()[1:]
    sigma = np.std(Returns) * np.sqrt(252)
    print(f"Volatility for {indexName} in the given period is {sigma}\n")


def Market(Market, marketName):
    filt = Market['Date'] >= '2018-12-1'
    Market_last_month = Market.loc[filt]
    volatility_list = np.zeros(10)
    for i in range(10):
        # volatility calculation
        Returns = Market_last_month.iloc[:, i + 1].pct_change()[1:]
        volatility_list[i] = np.std(Returns) * np.sqrt(252)
    Market_vol_df = pd.DataFrame({'Company': Market.columns[1:], 'Volatility': volatility_list})
    print(f"Volatility for various stocks in {marketName} in the given period is as follows:")
    print(Market_vol_df)
    print("\n")


Index(snx, "Sensex")
Index(nifty, "Nifty")
Market(bse, "BSE")
Market(nse, "NSE")
