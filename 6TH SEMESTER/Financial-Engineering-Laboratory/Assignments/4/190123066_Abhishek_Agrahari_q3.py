import pandas as pd
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from IPython.display import display

plt.style.use('seaborn')

data = pd.read_csv('data.csv', usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
returns = data.pct_change()
meanReturns = np.array(returns.mean()) * 12
covMatrix = np.array(returns.cov()) * 12


def Return(w):
    returns = np.sum(meanReturns * w)
    return returns


def Risk(w):
    std = np.sqrt(np.dot(w.T, np.dot(covMatrix, w)))
    return std


def weightConstraint(w):
    weightSum = 0
    for i in range(10):
        weightSum += w[i]
    return weightSum - 1


def riskCalculator(returns):
    weights = np.zeros(10)
    for i in range(10):
        weights[i] = 0.1
    return minimize(fun=Risk,
                    x0=weights,
                    method='SLSQP',  # Sequential Least Squares Programming
                    constraints=[{'type': 'eq', 'fun': weightConstraint},
                                 {'type': 'eq', 'fun': lambda w, expectedReturn: Return(w) - expectedReturn, 'args': np.array([returns])}])


def sharpeRatio(w):
    mean = Return(w)
    risk = Risk(w)
    return (mean - 0.05) / risk


def tangencyPortfolio():
    weights = np.zeros(10)
    for i in range(10):
        weights[i] = 0.1
    return minimize(fun=lambda w: -1 * sharpeRatio(w),
                    x0=weights,
                    method='SLSQP',
                    constraints={'type': 'eq', 'fun': weightConstraint})


print("Part a - figure")
N1 = 100
returns1 = np.linspace(-1, 1.5, N1)
stddev1 = np.zeros(N1)
for i in range(N1):
    stddev1[i] = riskCalculator(returns1[i]).fun
TipOfBullet = stddev1.argmin()
fig1, ax1 = plt.subplots()
ax1.plot(stddev1[TipOfBullet:], returns1[TipOfBullet:])
ax1.set_xlabel('Standard Deviation (Risk)')
ax1.set_ylabel('Returns')
ax1.set_title('Markowitz Efficient Frontier')

print("\nPart b")
val = tangencyPortfolio()
print(f"Market Portfolio has Risk = {round(Risk(val.x),5)}, Return = {round(Return(val.x),5)} with following weights on assets - ")
df = pd.DataFrame({'Company': data.columns, 'Weights on their stocks': val.x})
display(df)
# for i in range(10):
#     print(round(val.x[i], 3), end=" ")

print("\n\nPart c - Figure")
X = np.arange(0, 1, 0.01)
Y = -1 * val.fun * X + 0.05
fig2, ax2 = plt.subplots()
ax2.plot(stddev1, returns1, label='Minimum Variance Curve')
ax2.plot(X, Y, label='Capital Market Line')
ax2.set_xlabel('Standard Deviation (Risk)')
ax2.set_ylabel('Returns')
ax2.scatter([Risk(val.x)], [Return(val.x)], label='Market Portfolio')
ax2.scatter([0], [0.05], label='Risk Free Asset')
ax2.legend()
ax2.set_title('Minimum Variance Curve and Capital Market Line')

print("\nPart d - Figure")
fig3, ax3 = plt.subplots()
beta = np.arange(-2, 2.1, 0.1)
for i in range(meanReturns.shape[0]):
    mean = meanReturns[i]
    muv = 0.05 + (mean - 0.05) * beta
    ax3.plot(beta, muv, label=data.columns[i])
ax3.set_title('Security Market Line for all the 10 assets')
ax3.set_xlabel('Beta coefficient (β)')
ax3.set_ylabel('Value of Return (μ)')
ax3.legend()
plt.show()
