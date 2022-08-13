import pandas as pd
import numpy as np
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from IPython.display import display
import seaborn
seaborn.set()

# part a)
data = pd.read_csv('midsemdata.csv', usecols=[1, 2, 3, 4])
returns = data.pct_change().iloc[1:, ]
MeanReturn = returns.mean()
CovMatrix = returns.cov()
print(MeanReturn)
print(CovMatrix)
marketPortReturn = returns.mean().iloc[0]
print(f"\nMean return for market index - {marketPortReturn}")
print(f"Variance for market index - {returns.cov().iloc[0][0]}\n")

# part b
Rf = 0.04
beta = np.zeros(3)
alpha = np.zeros(3)
unsystematic_risk = np.zeros(3)
for i in range(3):
    beta[i] = CovMatrix.iloc[i + 1][0] / CovMatrix.iloc[0][0]
    print(f"Beta for Stock {i+1} is {beta[i]}")
    alpha[i] = MeanReturn.iloc[i + 1] - beta[i] * marketPortReturn
    print(f"Alpha for Stock {i+1} is {alpha[i]}")
    Systematic_risk = beta[i] * np.sqrt(CovMatrix.iloc[0][0])
    print(f"Systematic_risk for Stock {i+1} is {Systematic_risk}")
    unsystematic_risk[i] = np.sqrt(returns.cov().iloc[i + 1][i + 1] - Systematic_risk**2)
    print(f"Unsystematic_risk for Stock {i+1} is {unsystematic_risk[i]}\n")

# part c
df = pd.read_csv('midsemdata.csv', usecols=[2, 3, 4])
Return = df.pct_change()
u = [[1, 1, 1]]
m = np.zeros([1, 3])
m[0] = np.array(Return.mean())
C = np.array(Return.cov())


def getReturn(weights):
    returns = np.sum(m * weights)
    return returns


def getRisk(weights):
    std = np.sqrt(np.dot(weights, np.dot(C, np.transpose(weights))))
    return std


w = []
returns = []
risks = []
W1 = []
W2 = []
W3 = []

for i in range(1000):
    w = np.random.random(3)
    wsum = np.sum(w)
    w = w / wsum
    W1.append(w[0])
    W2.append(w[1])
    W3.append(w[2])
    rate = getReturn(w)
    risk = getRisk(w)
    returns.append(rate)
    risks.append(risk)

fig = plt.figure()
fig.set_size_inches(12, 8)
ax = fig.add_subplot(projection='3d')
ax.scatter(W1, W2, returns, color='green')
ax.set_xlabel('weight of stock 1')
ax.set_ylabel('weight of stcok 2')
ax.set_zlabel('return rate of the portfolio')
ax.set_title('return of all attainable possible portfolios using the three stocks (with short sales allowed)')
plt.show()

fig = plt.figure()
fig.set_size_inches(12, 8)
ax = fig.add_subplot(projection='3d')
ax.scatter(W1, W2, risk, color='blue')
ax.set_xlabel('weight of stock 1')
ax.set_ylabel('weight of stcok 2')
ax.set_zlabel('risk of the portfolio')
ax.set_title('risk of all possible attainable portfolios using the three stocks (with short sales allowed)')
plt.show()

# part d
# Mean and variance for market
market = pd.read_csv('midsemdata.csv', usecols=[1])
market_r = np.array(market.pct_change().mean())
market_C = np.array(market.pct_change().cov())

C_ = np.linalg.inv(C)  # inverse of C
# minimum variance portfolio
w = np.dot(u, C_) / np.dot(u, np.dot(C_, np.transpose(u)))
print('\nWeights in minimum variance portfolio : \n', w)
print('\nrisk in minimum variance portfolio : \n', getRisk(w))
print('\nreturn in minimum variance portfolio : \n', getReturn(w))
print('\nmarket risk : \n', np.sqrt(market_C))
print('\nmarket return : \n', market_r)
