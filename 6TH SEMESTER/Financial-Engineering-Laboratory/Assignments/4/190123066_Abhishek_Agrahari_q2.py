import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from IPython.display import display
from scipy.optimize import minimize
plt.style.use('seaborn')
M = np.array([0.1, 0.2, 0.15])
C = np.array([[0.005, -0.010, 0.004], [-0.010, 0.040, -0.002], [0.004, -0.002, 0.023]])


def Risk_3assets(w):
    variance = 0
    for i in range(3):
        for j in range(3):
            variance += w[i] * w[j] * C[i][j]
    return np.sqrt(variance)


def Return_3assets(w):
    mean = 0
    for i in range(3):
        mean += w[i] * M[i]
    return mean


def riskCalculator_3_assets(returns):
    x0 = np.array([0.3, 0.3, 0.4])
    return minimize(fun=Risk_3assets,
                    x0=x0,
                    method='SLSQP',  # Sequential Least Squares Programming
                    constraints=[{'type': 'eq', 'fun': lambda w: w[0] + w[1] + w[2] - 1},
                                 {'type': 'eq', 'fun': lambda w, expectedReturn: Return_3assets(w) - expectedReturn, 'args': np.array([returns])}])


def riskCalculator_2_assets(returns, i, j):
    x0 = np.array([0.5, 0.5])
    return minimize(fun=lambda w: np.sqrt(w[0] * w[0] * C[i][i] + w[1] * w[1] * C[j][j] + 2 * w[0] * w[1] * C[i][j]),
                    x0=x0,
                    method='SLSQP',  # Sequential Least Squares Programming
                    constraints=[{'type': 'eq', 'fun': lambda w: w[0] + w[1] - 1},
                                 {'type': 'eq', 'fun': lambda w, expectedReturn: w[0] * M[i] + w[1] * M[j] - expectedReturn, 'args': np.array([returns])}])


def FeasibleRegion():
    N = 100000
    returns = np.zeros(N)
    risk = np.zeros(N)
    for i in range(N):
        w = np.random.random(3)
        w = w / np.sum(w)
        returns[i] = Return_3assets(w)
        risk[i] = Risk_3assets(w)
    return risk, returns



# construct the minimum variance curve
N = 250
returns = np.linspace(0.05, 0.25, N)
returnPlot1 = []
stdPlot1 = []
for i in range(N):
    val = riskCalculator_3_assets(returns[i])
    if(val.x[0] >= 0 and val.x[1] >= 0 and val.x[2] >= 0):
        stdPlot1.append(val.fun)
        returnPlot1.append(returns[i])
fig1, ax1 = plt.subplots()
ax1.plot(stdPlot1, returnPlot1, label="Efficient Frontier")
ax1.set_xlabel('Standard Deviation')
ax1.set_ylabel('Returns')
ax1.set_title('Markowitz Efficient Frontier')


returnPlot, stdPlot = [], []
w0, w1 = [], []
fig2, ax2 = plt.subplots()
for k in range(N):
    val = riskCalculator_2_assets(returns[k], 0, 1)
    if(val.x[0] >= 0 and val.x[1] >= 0):
        stdPlot.append(val.fun)
        returnPlot.append(returns[k])
        w0.append(val.x[0])
        w1.append(val.x[1])
ax1.plot(stdPlot, returnPlot, label="MVC: 1 & 2")
ax2.plot(w0, w1)
ax2.set_xlabel('Weight on asset 1')
ax2.set_ylabel('Weight on asset 2')
ax2.set_title('Weights corresponding to MVC: 1 & 2')

returnPlot = []
stdPlot = []
w1, w2 = [], []
fig3, ax3 = plt.subplots()
for k in range(N):
    val = riskCalculator_2_assets(returns[k], 1, 2)
    if(val.x[0] >= 0 and val.x[1] >= 0):
        stdPlot.append(val.fun)
        returnPlot.append(returns[k])
        w1.append(val.x[0])
        w2.append(val.x[1])
ax1.plot(stdPlot, returnPlot, label="MVC: 2 & 3")
ax3.plot(w1, w2)
ax3.set_xlabel('Weight on asset 2')
ax3.set_ylabel('Weight on asset 3')
ax3.set_title('Weights corresponding to MVC: 2 & 3')

returnPlot = []
stdPlot = []
w0, w2 = [], []
fig4, ax4 = plt.subplots()
for k in range(N):
    val = riskCalculator_2_assets(returns[k], 0, 2)
    if(val.x[0] >= 0 and val.x[1] >= 0):
        stdPlot.append(val.fun)
        returnPlot.append(returns[k])
        w0.append(val.x[0])
        w2.append(val.x[1])
ax1.plot(stdPlot, returnPlot, label="MVC: 1 & 3")
ax4.plot(w0, w2)
ax4.set_xlabel('Weight on asset 1')
ax4.set_ylabel('Weight on asset 3')
ax4.set_title('Weights corresponding to MVC: 1 & 3')

riskFR, returnsFR = FeasibleRegion()
ax1.scatter(riskFR, returnsFR, s=10, label='Feasible Region', color='lightgoldenrodyellow')
ax1.legend()
plt.show()
