import pandas as pd
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from IPython.display import display

plt.style.use('seaborn')


def Return(w, meanReturns, covMatrix):
    returns = np.sum(meanReturns * w)
    return returns


def Risk(w, meanReturns, covMatrix):
    std = np.sqrt(np.dot(w.T, np.dot(covMatrix, w)))
    return std


def weightConstraint(w, meanReturns, covMatrix):
    weightSum = 0
    for i in range(10):
        weightSum += w[i]
    return weightSum - 1


def riskCalculator(returns, meanReturns, covMatrix):
    weights = np.zeros(10)
    for i in range(10):
        weights[i] = 0.1
    return minimize(fun=Risk,
                    x0=weights,
                    method='SLSQP',  # Sequential Least Squares Programming
                    constraints=[{'type': 'eq', 'fun': weightConstraint, 'args': (meanReturns, covMatrix)},
                                 {'type': 'eq', 'fun': lambda w, expectedReturn: Return(w, meanReturns, covMatrix) - expectedReturn, 'args': np.array([returns])}],
                    args=(meanReturns, covMatrix))


def sharpeRatio(w, meanReturns, covMatrix):
    mean = Return(w, meanReturns, covMatrix)
    risk = Risk(w, meanReturns, covMatrix)
    return (mean - 0.05) / risk


def tangencyPortfolio(meanReturns, covMatrix):
    weights = np.zeros(10)
    for i in range(10):
        weights[i] = 0.1
    return minimize(fun=lambda w, meanReturns, covMatrix: -1 * sharpeRatio(w, meanReturns, covMatrix),
                    x0=weights,
                    method='SLSQP',
                    constraints={'type': 'eq', 'fun': weightConstraint, 'args': (meanReturns, covMatrix)},
                    args=(meanReturns, covMatrix)
                    )


def solution(data, data_type):
    print("----------------------------------------------------------------\n")
    print(f"For {data_type} - ")
    print("\nPart a - figure")
    returns = data.pct_change()
    meanReturns = np.array(returns.mean()) * 12
    covMatrix = np.array(returns.cov()) * 12
    N1 = 100
    returns1 = np.linspace(-1, 1.5, N1)
    stddev1 = np.zeros(N1)
    for i in range(N1):
        stddev1[i] = riskCalculator(returns1[i], meanReturns, covMatrix).fun
    TipOfBullet = stddev1.argmin()
    fig1, ax1 = plt.subplots()
    ax1.plot(stddev1[TipOfBullet:], returns1[TipOfBullet:])
    ax1.set_xlabel('Standard Deviation (Risk)')
    ax1.set_ylabel('Returns')
    ax1.set_title(f"Markowitz Efficient Frontier ({data_type})")

    print("\nPart b")
    val = tangencyPortfolio(meanReturns, covMatrix)
    Market_Portforlio_Return = Return(val.x, meanReturns, covMatrix)
    print(f"Market Portfolio has Risk = {round(Risk(val.x, meanReturns, covMatrix),5)}, Return = {round(Market_Portforlio_Return,5)} with following weights on assets - ")
    df = pd.DataFrame({f"{data_type}": data.columns, 'Weights on their stocks': val.x})
    display(df)

    print("\n\nPart c - Figure")
    X = np.arange(0, 1, 0.01)
    Y = -1 * val.fun * X + 0.05
    fig2, ax2 = plt.subplots()
    ax2.plot(stddev1, returns1, label='Minimum Variance Curve')
    ax2.plot(X, Y, label='Capital Market Line')
    ax2.set_xlabel('Standard Deviation (Risk)')
    ax2.set_ylabel('Returns')
    ax2.scatter([Risk(val.x, meanReturns, covMatrix)], [Return(val.x, meanReturns, covMatrix)], label='Market Portfolio')
    ax2.scatter([0], [0.05], label='Risk Free Asset')
    ax2.legend()
    ax2.set_title(f'Minimum Variance Curve and Capital Market Line ({data_type})')

    print("\nPart d - Figure")
    fig3, ax3 = plt.subplots()
    Rf = 0.05
    beta = np.linspace(-1, 2.1, 40)
    slope = (Market_Portforlio_Return - Rf)
    ax3.plot(beta, slope * beta + Rf)
    for i in range(meanReturns.shape[0]):
        mean_val = meanReturns[i]
        beta_val = (mean_val - Rf) / (Market_Portforlio_Return - Rf)
        ax3.scatter(beta_val, mean_val, label=data.columns[i])
    ax3.set_title(f'Security Market Line for all the 10 assets ({data_type})')
    ax3.set_xlabel('Beta coefficient (β)')
    ax3.set_ylabel('Value of Return (μ)')
    ax3.legend()


sensex = pd.read_csv('bse/stocks_in_sensex.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
solution(sensex, 'Sensex Companies')

non_sensex = pd.read_csv('bse/stocks_not_in_sensex.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
solution(non_sensex, 'Non Sensex, BSE Companies')

nifty = pd.read_csv('nse/stocks_in_nifty.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
solution(nifty, 'Nifty Companies')

non_nifty = pd.read_csv('nse/stocks_not_in_nifty.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
solution(non_nifty, 'Non Nifty, NSE Companies')

plt.show()
