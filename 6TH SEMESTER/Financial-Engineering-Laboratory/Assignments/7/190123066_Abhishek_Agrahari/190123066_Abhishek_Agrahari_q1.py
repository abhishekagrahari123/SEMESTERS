import numpy as np
from scipy.stats import norm


def blackScholes(r, S, K, T, sigma, t):
    d1 = (np.log(S / K) + (r + (sigma**2) / 2) * (T - t)) / (sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    callp = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * (T - t)) * norm.cdf(d2, 0, 1)
    putp = K * np.exp(-r * (T - t)) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)

    return [callp, putp]


# define variables
T = 1
K = 1
r = 0.05
sigma = 0.6
t = 0  # time at which option price is required
S = 0.8  # Stock price at time t

optionPrices = blackScholes(r, S, K, T, sigma, t)
print("Call Option Price is ", optionPrices[0])
print("Put Option Price is ", optionPrices[1])
