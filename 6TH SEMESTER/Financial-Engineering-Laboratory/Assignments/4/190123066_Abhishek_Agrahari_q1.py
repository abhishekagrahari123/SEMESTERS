import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from IPython.display import display
from scipy.optimize import minimize
plt.style.use('seaborn')

M = np.array([0.1, 0.2, 0.15])
C = np.array([[0.005, -0.010, 0.004], [-0.010, 0.040, -0.002], [0.004, -0.002, 0.023]])
# we will vary w1, w2, w3 such that w1 + w2 + w3 = 1
# return = w[1]*E[X1] + w[2]*E[X2] + w[3]*E[X3]
# variance = summation w[i]*w[j]*C[i,j]


def Risk(w):
    variance = 0
    for i in range(3):
        for j in range(3):
            variance += w[i] * w[j] * C[i][j]
    return np.sqrt(variance)


def Return(w):
    mean = 0
    for i in range(3):
        mean += w[i] * M[i]
    return mean


def riskCalculator(returns):
    x0 = np.array([0.3, 0.3, 0.4])
    return minimize(fun=Risk,
                    x0=x0,
                    method='SLSQP',  # Sequential Least Squares Programming
                    constraints=[{'type': 'eq', 'fun': lambda w: w[0] + w[1] + w[2] - 1},
                                 {'type': 'eq', 'fun': lambda w, expectedReturn: Return(w) - expectedReturn, 'args': np.array([returns])}])

# if ind = -1 it will calculate maximum return and if ind = 1 it will calculate minimum return


def returnCalculator(stddev, ind):
    x0 = np.array([0.3, 0.3, 0.4])
    return minimize(fun=lambda w: ind * Return(w),
                    x0=x0,
                    method='SLSQP',
                    constraints=[{'type': 'eq', 'fun': lambda w: w[0] + w[1] + w[2] - 1},
                                 {'type': 'eq', 'fun': lambda w, expectedRisk: Risk(w) - expectedRisk, 'args': np.array([stddev])}])


def sharpeRatio(w):
    mean = Return(w)
    risk = Risk(w)
    return (mean - 0.1) / risk


def tangencyPortfolio():
    x0 = np.array([0.3, 0.3, 0.4])
    return minimize(fun=lambda w: -1 * sharpeRatio(w),
                    x0=x0,
                    method='SLSQP',
                    constraints={'type': 'eq', 'fun': lambda w: w[0] + w[1] + w[2] - 1})


# (a)
print("Part a - figure")
N1 = 100
returns1 = np.linspace(0, 0.5, N1)
stddev1 = np.zeros(N1)
for i in range(N1):
    stddev1[i] = riskCalculator(returns1[i]).fun
TipOfBullet = stddev1.argmin()
fig1, ax1 = plt.subplots()
ax1.plot(stddev1[TipOfBullet:], returns1[TipOfBullet:])
ax1.set_xlabel('Standard Deviation (Risk)')
ax1.set_ylabel('Returns')
ax1.set_title('Markowitz Efficient Frontier')

# (b)
print("\nPart b")
N2 = 10
returnsTab = np.zeros(N2)
stddevTab = np.zeros(N2)
w1 = np.zeros(N2)
w2 = np.zeros(N2)
w3 = np.zeros(N2)
k = TipOfBullet + 1
for i in range(N2):
    val = riskCalculator(returns1[k])
    stddevTab[i] = val.fun
    returnsTab[i] = returns1[k]
    w1[i], w2[i], w3[i] = val.x
    k = k + 1
df = pd.DataFrame({'Returns': returnsTab, 'Standard Deviation': stddevTab, 'W1': w1, 'W2': w2, 'W3': w3})
display(df)


# (c)
print("\nPart c")
val = returnCalculator(0.15, -1)
print(f"Maximum Return would be {round(-100 * val.fun,4)}% and corresponding weights of the assets would be {round(val.x[0],4)},{round(val.x[1],4)},{round(val.x[2],4)}")
val = returnCalculator(0.15, 1)
print(f"Minimum Return would be {round(100 * val.fun,4)}% and corresponding weights of the assets would be {round(val.x[0],4)},{round(val.x[1],4)},{round(val.x[2],4)}")

# (d)
print("\nPart d")
val = riskCalculator(0.18)
print(f"Minimum Risk would be {round(100 * val.fun,4)}% and corresponding weights of the assets would be {round(val.x[0],4)},{round(val.x[1],4)},{round(val.x[2],4)}")

# (e)
# we want to maximize the sharpe ratio (Return - r)/Risk
print("\nPart e")
val = tangencyPortfolio()
print(f"Market Portfolio has Risk = {round(Risk(val.x),4)}, Return = {round(Return(val.x),4)} with following weights on assets - {round(val.x[0],4)},{round(val.x[1],4)},{round(val.x[2],4)}")
X = np.arange(0, 0.6, 0.01)
Y = -1 * val.fun * X + 0.1
fig2, ax2 = plt.subplots()
ax2.plot(stddev1, returns1, label='Minimum Variance Curve')
ax2.plot(X, Y, label='Capital Market Line')
ax2.set_xlabel('Standard Deviation (Risk)')
ax2.set_ylabel('Returns')
ax2.scatter([Risk(val.x)], [Return(val.x)], label='Market Portfolio')
ax2.scatter([0], [0.1], label='Risk Free Asset')
ax2.set_title('Minimum Variance Curve and Capital Market Line')
ax2.legend()
plt.show()

# (f)
print("\nPart f")
riskInRiskyAsset = Risk(val.x)
weightDist = val.x
for risk in [0.1, 0.25]:
    weightOnRiskyAsset = risk / riskInRiskyAsset
    weightsRisky = [weightOnRiskyAsset * element for element in weightDist]
    weightOnRiskFreeAsset = 1 - weightOnRiskyAsset
    print(f"For {risk} risk - Weight on risk free asset = {round(weightOnRiskFreeAsset,4)}, weights on risky asset = {round(weightsRisky[0],4)},{round(weightsRisky[1],4)},{round(weightsRisky[2],4)}")
