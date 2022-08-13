import numpy as np
from scipy.stats import norm
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
pd.options.mode.chained_assignment = None
plt.style.use('seaborn')


def N(x):
    return norm.cdf(x)


def BSM(S0, sigma, K, T, r):
    if T == 0:
        call = max(0, S0 - K)
    else:
        d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        call = N(d1) * S0 - N(d2) * K * np.exp(-r * T)
    return call


def Vega(S0, sigma, K, T, r):
    d1 = (np.log(S0 / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return np.sqrt(T) * K * np.exp(-r * T) * (1 / np.sqrt(2 * np.pi)) * np.exp(-(d2**2) / 2)


def implied_vol(S0, K, T, r, market_price, tol=0.00001):
    max_iter = 200  # max no. of iterations
    vol_old = 0.3  # initial guess
    for k in range(max_iter):
        bs_price = BSM(S0, vol_old, K, T, r)
        Cprime = Vega(S0, vol_old, K, T, r)
        C = bs_price - market_price
        vol_new = vol_old - C / Cprime
        if (abs(vol_old - vol_new) < tol):
            break
        vol_old = vol_new
    implied_vol = vol_new
    return implied_vol


def adjustTTM(x):
    y = x.days
    y = float(y)
    return y / 365


r = 0.05


def dataframe_cleaning(df):
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiry'] = pd.to_datetime(df['Expiry'])
    df['TTM'] = df['Expiry'] - df['Date']
    df.drop(columns=['Expiry'], inplace=True)
    df['TTM'] = df['TTM'].apply(adjustTTM)


def meanImpliedVolatility(df):
    impvol = np.zeros(df.shape[0])
    for i in range(df.shape[0]):
        impvol[i] = implied_vol(df.iloc[i]['Underlying Value'], df.iloc[i]['Strike'], df.iloc[i]['TTM'], r, df.iloc[i]['Call'])
    df['Imp Vol'] = impvol
    df.dropna(inplace=True)
    return np.mean(df['Imp Vol'])


def historicalVolatilityCalculator(data):
    Returns = data.pct_change()[1:]
    his_volatility = np.std(Returns) * np.sqrt(252)
    return his_volatility


na_vals = '-'
df_nifty = pd.read_csv('NIFTY-optiondata.csv', na_values=na_vals)
dataframe_cleaning(df_nifty)
df_stock = pd.read_csv('stockoptiondata.csv', na_values=na_vals)
dataframe_cleaning(df_stock)

df_ntpc = df_stock.loc[df_stock['Symbol'] == 'NTPC']

df_hcl = df_stock.loc[df_stock['Symbol'] == 'HCLTECH']

df_adaniport = df_stock.loc[df_stock['Symbol'] == 'ADANIPORTS']

imp1 = meanImpliedVolatility(df_nifty)
imp2 = meanImpliedVolatility(df_ntpc)
imp3 = meanImpliedVolatility(df_hcl)
imp4 = meanImpliedVolatility(df_adaniport)

underlyingAssetData = pd.read_csv('underlyingAssetData.csv')
his1 = historicalVolatilityCalculator(underlyingAssetData['Nifty'])
his2 = historicalVolatilityCalculator(underlyingAssetData['NTPC'])
his3 = historicalVolatilityCalculator(underlyingAssetData['HCLTECH'])
his4 = historicalVolatilityCalculator(underlyingAssetData['ADANIPORTS'])

df = pd.DataFrame()
impvol = [imp1, imp2, imp3, imp4]
hisvol = [his1, his2, his3, his4]
df['Underlying Asset'] = ['NIFTY', 'NTPC', 'HCLTECH', 'ADANIPORTS']
df['Implied Volatility'] = impvol
df['Historical Volatility'] = hisvol
print(df)
