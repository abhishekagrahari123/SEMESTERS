import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
from dateutil.relativedelta import relativedelta
from IPython.display import display
import seaborn as sns
sns.set(style="darkgrid")

snx = pd.read_csv('bse/sensex.csv', usecols=[0, 4])
nifty = pd.read_csv('nse/nifty.csv', usecols=[0, 4])
bse = pd.read_csv('bse/bse.csv')
nse = pd.read_csv('nse/nse.csv')

snx['Date'] = pd.to_datetime(snx['Date'])
nifty['Date'] = pd.to_datetime(nifty['Date'])
bse['Date'] = pd.to_datetime(bse['Date'])
nse['Date'] = pd.to_datetime(nse['Date'])


def N(x):
    return norm.cdf(x)


def BSM(x, sigma, K, t=0.5, r=0.05):
    if t == 0:
        call = max(0, x - K)
        put = max(0, K - x)
    else:
        d1 = (np.log(x / K) + (r + sigma**2 / 2) * t) / (sigma * np.sqrt(t))
        d2 = d1 - sigma * np.sqrt(t)
        call = N(d1) * x - N(d2) * K * np.exp(-r * t)
        put = call + K * np.exp(-r * t) - x
    return call, put


def Market(Market, marketName):
    for cidx in range(1, 11):
        for A in np.arange(0.5, 1.6, 0.1):
            fig, axs = plt.subplots(3, 1, figsize=(5, 12), sharex=True)
            axs = axs.flatten()
            startdate = datetime(2019, 1, 1)
            cp = np.zeros(60)
            pp = np.zeros(60)
            sig = np.zeros(60)
            for i in range(60):
                startdate = startdate - relativedelta(months=1)
                filt = Market['Date'] >= startdate
                Market_req = Market.loc[filt].iloc[:, cidx]
                Returns = Market_req.pct_change()[1:]
                sigma = np.std(Returns) * np.sqrt(252)
                sig[i] = sigma
                S0 = Market_req.iloc[-1]
                cp[i], pp[i] = BSM(S0, sigma, A * S0)
            axs[0].plot(np.arange(1, 61), cp, color='orange')
            axs[1].plot(np.arange(1, 61), pp, color='blue')
            axs[2].plot(np.arange(1, 61), sig, color='green')
            axs[0].set_ylabel('Call Prices')
            axs[1].set_ylabel('Put Prices')
            axs[2].set_ylabel('Volatility')
            fig.suptitle(f'{Market.columns[cidx]} ({marketName}): A = {round(A,1)}')
            fig.supxlabel('No. of months considered')
        plt.show()


def Index(Index, indexName):
    for A in np.arange(0.5, 1.6, 0.1):
        fig, axs = plt.subplots(3, 1, figsize=(5, 12), sharex=True)
        axs = axs.flatten()
        startdate = datetime(2019, 1, 1)
        cp = np.zeros(60)
        pp = np.zeros(60)
        sig = np.zeros(60)
        for i in range(60):
            startdate = startdate - relativedelta(months=1)
            filt = Index['Date'] >= startdate
            Index_req = Index.loc[filt]
            Returns = Index_req['Close'].pct_change()[1:]
            sigma = np.std(Returns) * np.sqrt(252)
            sig[i] = sigma
            S0 = Index_req.iloc[-1]['Close']
            cp[i], pp[i] = BSM(S0, sigma, A * S0)
        axs[0].plot(np.arange(1, 61), cp, color='orange')
        axs[1].plot(np.arange(1, 61), pp, color='blue')
        axs[2].plot(np.arange(1, 61), sig, color='green')
        axs[0].set_ylabel('Call Prices')
        axs[1].set_ylabel('Put Prices')
        axs[2].set_ylabel('Volatility')
        fig.suptitle(f'{indexName}: A = {round(A,1)}')
        fig.supxlabel('No. of months considered')
        plt.show()


Index(snx, "Sensex")
Index(nifty, "Nifty")
Market(bse, "BSE")
Market(nse, "NSE")
