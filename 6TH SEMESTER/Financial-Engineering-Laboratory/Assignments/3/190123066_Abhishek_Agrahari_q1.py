import numpy as np
import pandas as pd
import time
from IPython.display import display
from tabulate import tabulate


def print_V(V, M):
    print(tabulate(V))


def loopback_option_binomial_algo(S0, T, r, σ, M, print_values):
    start_time = time.time()
    dt = T / M
    u = np.exp(σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    d = np.exp(-σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    q = (np.exp(r * dt) - d) / (u - d)
    V = np.zeros((2**M, M + 1), dtype='O')
    print(f"u*d = {u*d}")
    for i in range(2**M):
        # every i represents a path
        S = np.zeros(M + 1)
        S[0] = S0
        maxi = S0
        for j in range(1, M + 1):
            S[j] = S[j - 1]
            if (i & (1 << (M - j))):
                S[j] *= u
            else:
                S[j] *= d
            maxi = max(maxi, S[j])
        V[i][M] = maxi - S[M]
    for i in range(M - 1, -1, -1):
        for j in range(1 << M):
            if j < (1 << i):
                V[j][i] = np.exp(-r * dt) * (q * V[2 * j + 1][i + 1] + (1 - q) * V[2 * j][i + 1])
            else:
                V[j][i] = ' '
    end_time = time.time()

    if print_values:
        print_V(V, M)
    return V[0][0], end_time - start_time


S0 = 100
T = 1
r = 0.08
σ = 0.2

# (a)
M = [5, 10]
for m in M:
    price, time_req = loopback_option_binomial_algo(S0, T, r, σ, m, False)
    print(f"Value of the loopback option for M = {m} is {price} and time required to compute this is {time_req*1000} milliseconds")

# (b)
prices = []
for m in range(5, 16, 1):
    price, _ = loopback_option_binomial_algo(S0, T, r, σ, m, False)
    prices.append(price)
df = pd.DataFrame({'M': range(5, 16, 1), 'Loopback Option Price': prices})
display(df)

# (c)
print(f"\nValues of the options for M = 5 is - ")
loopback_option_binomial_algo(S0, T, r, σ, 5, True)
