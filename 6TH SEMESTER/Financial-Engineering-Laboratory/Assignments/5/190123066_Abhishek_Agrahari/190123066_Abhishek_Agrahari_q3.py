import pandas as pd
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from IPython.display import display
import statistics
plt.style.use('seaborn')


def solution(indices, non_indices, market):
    # Returns and covariance calculation
    indices_returns = indices.pct_change()
    non_indices_returns = non_indices.pct_change()
    indices_meanReturns = np.array(indices_returns.mean()) * 12
    indices_covMatrix = np.array(indices_returns.cov()) * 12
    non_indices_meanReturns = np.array(non_indices_returns.mean()) * 12
    non_indices_covMatrix = np.array(non_indices_returns.cov()) * 12
    market_portfolio_ret = indices_meanReturns[0]
    market_portfolio_var = indices_covMatrix[0][0]
    Rf = 0.05     # risk free rate

    beta_array = np.zeros(11)
    for i in range(11):
        beta_array[i] = indices_covMatrix[i][0] / market_portfolio_var
    df = pd.DataFrame({f"{market} Indices Stocks": indices.columns[1:], 'Beta': beta_array[1:]})
    display(df)
    print("\n")

    for i in range(11):
        beta_array[i] = non_indices_covMatrix[i][0] / market_portfolio_var
    df = pd.DataFrame({f"{market} Non-Indices Stocks": non_indices.columns[1:], 'Beta': beta_array[1:]})
    display(df)
    print("\n")


bse_indices = pd.read_csv('./bse/sensex.csv').iloc[:, 4]
sensex = pd.read_csv('bse/stocks_in_sensex.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
sensex.insert(0, "MARKET PORTFOLIO", bse_indices)
non_sensex = pd.read_csv('bse/stocks_not_in_sensex.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
non_sensex.insert(0, "MARKET PORTFOLIO", bse_indices)
solution(sensex, non_sensex, "BSE")

nse_indices = pd.read_csv('./nse/nifty.csv').iloc[:, 5]
nifty = pd.read_csv('nse/stocks_in_nifty.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
nifty.insert(0, "MARKET PORTFOLIO", nse_indices)
non_nifty = pd.read_csv('nse/stocks_not_in_nifty.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
non_nifty.insert(0, "MARKET PORTFOLIO", nse_indices)
solution(nifty, non_nifty, "NSE")
plt.show()
