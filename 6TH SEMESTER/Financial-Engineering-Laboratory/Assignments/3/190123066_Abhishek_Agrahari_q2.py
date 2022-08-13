import numpy as np
import time
import pandas as pd
from IPython.display import display
from matplotlib import pyplot as plt

S0 = 100
T = 1
r = 0.08
σ = 0.2

dp = {}


def loopback_option_markov_algo(step, SP, maxSP, u, d, q, dt, M):
    if step == M:
        return maxSP - SP
    elif dp.get((SP, maxSP)) != None:
        return dp.get((SP, maxSP))
    else:
        up = loopback_option_markov_algo(step + 1, SP * u, max(SP * u, maxSP), u, d, q, dt, M)
        down = loopback_option_markov_algo(step + 1, SP * d, max(SP * d, maxSP), u, d, q, dt, M)
        dp[SP, maxSP] = np.exp(-r * dt) * (q * up + (1 - q) * down)
        return dp[SP, maxSP]


def loopback_option(M):
    dt = T / M
    u = np.exp(σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    d = np.exp(-σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    q = (np.exp(r * dt) - d) / (u - d)
    dp.clear()
    start_time = time.time()
    price = loopback_option_markov_algo(0, S0, S0, u, d, q, dt, M)
    end_time = time.time()
    time_req = end_time - start_time
    return price, time_req


M = [5, 10, 25, 50]
prices = []
times = []
for m in M:
    price, time_req = loopback_option(m)
    prices.append(price)
    times.append(time_req)
df = pd.DataFrame({'M': M, 'Initial Option Price': prices, 'Time Required(in milliseconds)': times})
display(df)

prices = []
for m in range(5, 31, 1):
    price, _ = loopback_option(m)
    prices.append(price)
plt.plot(range(5, 31, 1), prices)
plt.xlabel('M')
plt.ylabel('Initial option price')
plt.title('Initial option price vs M')
plt.tight_layout()
plt.show()
