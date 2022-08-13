import pandas as pd
import numpy as np
import math
from scipy.optimize import minimize
from matplotlib import pyplot as plt
from IPython.display import display
from tabulate import tabulate


def calculate_u_and_d(sigma, r, dt):
    u = np.exp(sigma * math.sqrt(dt))
    d = np.exp(-sigma * math.sqrt(dt))
    return u, d


def calculate_option_price(u, d, p, M, dt, S, r, i, min_S, dp, K):
    if i == M:
        payoff = max(0, K - min_S)
        if payoff > 0:
            return payoff
        else:
            return 0
    elif dp.get((i, S, min_S)) != None:
        return dp.get((i, S, min_S))
    else:
        dp[i, S, min_S] = np.exp(-r * dt) * (p * calculate_option_price(u, d, p, M, dt, S * u, r, i + 1, min(min_S, S * u), dp, K) + (1 - p) * calculate_option_price(u, d, p, M, dt, S * d, r, i + 1, min(min_S, S * d), dp, K))
        return dp[i, S, min_S]


def print_V(V, M):
    print(tabulate(V))


def loopback_option_binomial_algo(S0, T, r, σ, K, M, print_values):
    dt = T / M
    u, d = calculate_u_and_d(sigma, r, dt)
    q = (np.exp(r * dt) - d) / (u - d)
    V = np.zeros((2**M, M + 1), dtype='O')
    for i in range(2**M):
        # every i represents a path
        S = np.zeros(M + 1)
        S[0] = S0
        mini = S0
        for j in range(1, M + 1):
            S[j] = S[j - 1]
            if (i & (1 << (M - j))):
                S[j] *= u
            else:
                S[j] *= d
            mini = min(mini, S[j])
        V[i][M] = max(0, K - mini)
    for i in range(M - 1, -1, -1):
        for j in range(1 << M):
            if j < (1 << i):
                V[j][i] = np.exp(-r * dt) * (q * V[2 * j + 1][i + 1] + (1 - q) * V[2 * j][i + 1])
            else:
                V[j][i] = ' '

    if print_values:
        print_V(V, M)
    return V[0][0]


S0 = 100.0
K = 95.0
T = 1
r = 0.04
sigma = 0.25
M = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# part a)
data = pd.DataFrame(columns=['M', 'Price'])
for m in M:
    dt = T / m
    u, d = calculate_u_and_d(sigma, r, dt)
    p = (np.exp(r * dt) - d) / (u - d)

    if d < np.exp(r * dt) and np.exp(r * dt) < u:
        dp = {}
        price = loopback_option_binomial_algo(S0, T, r, sigma, K, m, 0)
        data.loc[len(data)] = [m, price]
    else:
        print("There is arbitrage for M = %d" % m)
print(data)

# part b)
loopback_option_binomial_algo(S0, T, r, sigma, K, 5, 1)

# part c)
m = 5
K = np.arange(50, 150, 1)
option_price = np.zeros(K.shape[0])

for i in range(K.shape[0]):
    dt = T / m
    u, d = calculate_u_and_d(sigma, r, dt)
    p = (np.exp(r * dt) - d) / (u - d)

    if d < np.exp(r * dt) and np.exp(r * dt) < u:
        dp = {}
        option_price[i] = calculate_option_price(u, d, p, m, dt, S0, r, 0, S0, dp, K[i])
    else:
        print("There is arbitrage for M = %d" % m)

plt.plot(K, option_price)
plt.title('Plot of Europian option price at t=0 vs K ')
plt.ylabel('Price of Europian option')
plt.xlabel('Strike Price')
plt.show()


K = 95.0
T = 1
r = 0.04
sigma = 0.25
m = 5
S0 = np.arange(50, 150, 1)
option_price = np.zeros(S0.shape[0])

for i in range(S0.shape[0]):
    dt = T / m
    u, d = calculate_u_and_d(sigma, r, dt)
    p = (np.exp(r * dt) - d) / (u - d)

    if d < np.exp(r * dt) and np.exp(r * dt) < u:
        dp = {}
        option_price[i] = calculate_option_price(u, d, p, m, dt, S0[i], r, 0, S0[i], dp, K)
    else:
        print("There is arbitrage for M = %d" % m)

plt.plot(S0, option_price)
plt.title('Plot of Europian option price at t=0 vs S(0) ')
plt.xlabel('Stock Price at t = 0')
plt.ylabel('Price of Europian option')
plt.show()

K = 95.0
T = 1
S0 = 100
sigma = 0.25
m = 5
r = np.arange(0.001, 0.2, 0.01)
option_price = np.zeros(r.shape[0])

for i in range(r.shape[0]):
    dt = T / m
    u, d = calculate_u_and_d(sigma, r[i], dt)
    p = (np.exp(r[i] * dt) - d) / (u - d)

    if d < np.exp(r[i] * dt) and np.exp(r[i] * dt) < u:
        dp = {}
        option_price[i] = calculate_option_price(u, d, p, m, dt, S0, r[i], 0, S0, dp, K)
    else:
        print("There is arbitrage for M = %d" % m)

plt.plot(r, option_price)
plt.title('Plot of Europian option price at t=0 vs r')
plt.xlabel('r')
plt.ylabel('Price of Europian option')
plt.show()

S0 = 100.0
T = 1
r = 0.04
sigma = 0.25
m = 5
K = 95
sigma = np.arange(0.1, 2, 0.1)
option_price = np.zeros(sigma.shape[0])

for i in range(sigma.shape[0]):
    dt = T / m
    u, d = calculate_u_and_d(sigma[i], r, dt)
    p = (np.exp(r * dt) - d) / (u - d)

    if d < np.exp(r * dt) and np.exp(r * dt) < u:
        dp = {}
        option_price[i] = calculate_option_price(u, d, p, m, dt, S0, r, 0, S0, dp, K)
    else:
        print("There is arbitrage for M = %d" % m)

plt.plot(sigma, option_price)
plt.title('Plot of Europian option price at t=0 vs sigma ')
plt.xlabel('sigma')
plt.ylabel('Price of Europian option')
plt.show()
