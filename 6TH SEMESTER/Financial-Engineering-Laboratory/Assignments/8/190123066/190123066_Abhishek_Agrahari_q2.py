import pandas as pd
from datetime import datetime
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
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
    filt = Market['Date'] >= '2018-12-1'
    Market_last_month = Market.loc[filt]
    volatility_list = np.zeros(10)
    fig, axs = plt.subplots(5, 2, figsize=(6, 24), sharex=True)
    axs = axs.flatten()

    for ax in axs:
        ax.label_outer()
    for ax in axs:
        ax.yaxis.set_tick_params(which='both', labelbottom=True)

    for i in range(10):
        # volatility calculation
        Returns = Market_last_month.iloc[:, i + 1].pct_change()[1:]
        volatility_list[i] = np.std(Returns) * np.sqrt(252)
        sig = np.std(Returns) * np.sqrt(252)

        # find initial stock price
        S0 = Market.iloc[-1, i + 1]

        # find call and put option price for various K
        cp = np.zeros(11)
        pp = np.zeros(11)
        for j, A in enumerate(np.arange(0.5, 1.6, 0.1)):
            cp[j], pp[j] = BSM(S0, sig, A * S0)
        axs[i].plot(np.arange(0.5, 1.6, 0.1), cp, label='Call')
        axs[i].plot(np.arange(0.5, 1.6, 0.1), pp, label='Put')
        axs[i].set_title(f'{Market.columns[i+1]}')

    handles, labels = axs[0].get_legend_handles_labels()
    fig.legend(handles, labels)
    fig.supylabel('Option Prices')
    fig.supxlabel('A')
    fig.suptitle(f'{marketName}: A vs Option Prices')
    plt.show()


def Index(Index, indexName, axisNo):
    filt = Index['Date'] >= '2018-12-1'
    Index_last_month = Index.loc[filt]
    Returns = Index_last_month['Close'].pct_change()[1:]
    sigma = np.std(Returns) * np.sqrt(252)
    S0 = Index.iloc[-1]['Close']

    cp = np.zeros(11)
    pp = np.zeros(11)
    for i, A in enumerate(np.arange(0.5, 1.6, 0.1)):
        cp[i], pp[i] = BSM(S0, sigma, A * S0)
    axs[axisNo].set_title(f'{indexName}: A vs Option Prices')
    axs[axisNo].plot(np.arange(0.5, 1.6, 0.1), cp, label='Call Prices')
    axs[axisNo].plot(np.arange(0.5, 1.6, 0.1), pp, label='Put Prices')
    axs[axisNo].legend()


fig, axs = plt.subplots(1, 2, figsize=(10, 5))
Index(snx, "Sensex", 0)
Index(nifty, "Nifty", 1)
axs = axs.flatten()
for ax in axs:
    ax.set_xlabel('A')
    ax.set_ylabel('Option Prices')
for ax in axs:
    ax.label_outer()
plt.show()
Market(bse, "BSE")
Market(nse, "NSE")
