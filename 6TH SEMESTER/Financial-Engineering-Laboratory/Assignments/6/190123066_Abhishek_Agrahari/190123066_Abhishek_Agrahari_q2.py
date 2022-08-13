import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import scipy.stats as stats
import os
import seaborn as sns
sns.set(style="darkgrid")

bse_m = pd.read_csv('BSE/monthly.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
bse_m = bse_m.dropna()
bse_w = pd.read_csv('BSE/weekly.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
bse_w = bse_w.dropna()
bse_d = pd.read_csv('BSE/daily.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
bse_d = bse_d.dropna()
nse_m = pd.read_csv('NSE/monthly.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
nse_m = nse_m.dropna()
nse_w = pd.read_csv('NSE/weekly.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
nse_w = nse_w.dropna()
nse_d = pd.read_csv('NSE/daily.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
nse_d = nse_d.dropna()

BSE = [bse_m, bse_w, bse_d]
NSE = [nse_m, nse_w, nse_d]

Time_len = [len(bse_m.iloc[:, 0]), len(bse_w.iloc[:, 0]), len(bse_d.iloc[:, 0])]
intervals = ['Monthly', 'Weekly', 'Daily']
colors = ['orange', 'blue', 'green']


def returns_calculator(data):
    length = len(data)
    returns = np.zeros(length - 1)
    for k in range(length - 1):
        returns[k] = (data.iloc[k + 1] - data.iloc[k]) / data.iloc[k]
    return returns


def normalised_return_calculator(data):
    mean = np.mean(data)
    stddev = np.std(data)
    norm_returns = np.zeros(len(data))
    for k in range(len(data)):
        norm_returns[k] = (data[k] - mean) / stddev
    return norm_returns


Market = [BSE, NSE]
Market_name = ['BSE', 'NSE']

for z in range(2):
    for i in range(10):
        for j in range(3):
            data = Market[z][j].iloc[:, i]
            returns = returns_calculator(data)
            norm_returns = normalised_return_calculator(returns)
            plt.hist(norm_returns, bins='auto', density=True, label='Normalised Returns', color=colors[j])
            plt.xlabel(f'Normalised Returns ({intervals[j]} basis)')
            plt.ylabel('Frequency of Normalised Returns')
            plt.title(f'Histogram of Normalised Returns ({intervals[j]}) for {Market_name[z]} - {Market[z][j].columns[i]}')
            x_axis = np.linspace(-7, 7, 100)
            plt.plot(x_axis, stats.norm.pdf(x_axis, 0, 1), label='N(0,1)', color='black')
            plt.legend()
            # path = f'Plots/Question_2/{Market_name[z]}/{Market[z][j].columns[i]}/'
            # if not os.path.exists(path):
            #     os.makedirs(path)
            # plt.savefig(path + f'{intervals[j]}.png')
            plt.show()
