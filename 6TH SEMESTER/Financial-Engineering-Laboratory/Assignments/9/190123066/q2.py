import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
plt.style.use('seaborn')
pd.options.mode.chained_assignment = None


def adjustTTM(x):
    y = x.days
    y = float(y)
    return y / 365


def dataframe_cleaning(df):
    df.dropna(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Expiry'] = pd.to_datetime(df['Expiry'])
    df['TTM'] = df['Expiry'] - df['Date']
    df.drop(columns=['Expiry', 'Date'], inplace=True)
    df['TTM'] = df['TTM'].apply(adjustTTM)


def plot_maker(df, assetName, optionType):
    fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
    ax1.scatter(df['TTM'], df['Strike'], df[optionType])
    ax1.set_xlabel('Time to Maturity')
    ax1.set_ylabel('Strike Price')
    ax1.set_zlabel(f'{optionType} Price')
    ax1.set_title(f'{assetName}: {optionType} Price vs (Strike Price, Time to Maturity)')
    ax1.view_init(elev=10, azim=20)

    fig2, ax2 = plt.subplots()
    ax2.scatter(df['Strike'], df[optionType])
    ax2.set_xlabel('Strike Price')
    ax2.set_ylabel(f'{optionType} Price')
    ax2.set_title(f'{assetName}: {optionType} Price vs Strike Price')

    fig3, ax3 = plt.subplots()
    ax3.scatter(df['TTM'], df[optionType])
    ax3.set_xlabel('Time to Maturity')
    ax3.set_ylabel(f'{optionType} Price')
    ax3.set_title(f'{assetName}: {optionType} Price vs Time to Maturity')

    plt.show()


na_vals = '-'
df = pd.read_csv('NIFTY-optiondata.csv', na_values=na_vals)
dataframe_cleaning(df)
plot_maker(df, 'NIFTY', 'Call')
plot_maker(df, 'NIFTY', 'Put')

df_stock = pd.read_csv('stockoptiondata.csv', na_values=na_vals)
dataframe_cleaning(df_stock)

df_hcl = df_stock.loc[df_stock['Symbol'] == 'HCLTECH']
plot_maker(df_hcl, 'HCLTECH', 'Call')
plot_maker(df_hcl, 'HCLTECH', 'Put')

df_ntpc = df_stock.loc[df_stock['Symbol'] == 'NTPC']
plot_maker(df_ntpc, 'NTPC', 'Call')
plot_maker(df_ntpc, 'NTPC', 'Put')

df_adaniport = df_stock.loc[df_stock['Symbol'] == 'ADANIPORTS']
plot_maker(df_adaniport, 'ADANIPORTS', 'Call')
plot_maker(df_adaniport, 'ADANIPORTS', 'Put')
