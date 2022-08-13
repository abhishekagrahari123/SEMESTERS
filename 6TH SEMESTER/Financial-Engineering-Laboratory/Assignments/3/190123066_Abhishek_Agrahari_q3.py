import numpy as np
import time

S0 = 100
T = 1
r = 0.08
σ = 0.2
K = 100


def european_call_binomial_algo(step_no, SP, u, d, q, dt, M):
    if step_no == M:
        return max(SP - K, 0)
    else:
        up = european_call_binomial_algo(step_no + 1, SP * u, u, d, q, dt, M)
        down = european_call_binomial_algo(step_no + 1, SP * d, u, d, q, dt, M)
        return np.exp(-r * dt) * (q * up + (1 - q) * down)


def binomial_algo(M):
    dt = T / M
    u = np.exp(σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    d = np.exp(-σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    q = (np.exp(r * dt) - d) / (u - d)
    start_time = time.time()
    price = european_call_binomial_algo(0, 100, u, d, q, dt, M)
    end_time = time.time()
    return price, end_time - start_time


dp = {}


def european_call_markov_algo(step_no, up_cnt, SP, u, d, q, dt, M):
    if step_no == M:
        return max(SP - K, 0)
    elif dp.get((step_no, up_cnt)) != None:
        return dp[step_no, up_cnt]
    else:
        up = european_call_markov_algo(step_no + 1, up_cnt + 1, SP * u, u, d, q, dt, M)
        down = european_call_markov_algo(step_no + 1, up_cnt, SP * d, u, d, q, dt, M)
        dp[step_no, up_cnt] = np.exp(-r * dt) * (q * up + (1 - q) * down)
        return dp[step_no, up_cnt]


def markov_algo(M):
    dt = T / M
    u = np.exp(σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    d = np.exp(-σ * np.sqrt(dt) + (r - (σ * σ) / 2) * dt)
    q = (np.exp(r * dt) - d) / (u - d)
    dp.clear()
    start_time = time.time()
    price = european_call_markov_algo(0, 0, 100, u, d, q, dt, M)
    end_time = time.time()
    return price, end_time - start_time


M = [5, 10, 20]
for m in M:
    price, time_req = binomial_algo(m)
    print(f"Using Binomial algo, value of the European call option for M = {m} is {price} and time required to compute this is {1000*time_req} milliseconds.")

M = [5, 10, 20, 25, 50, 100]
for m in M:
    price, time_req = markov_algo(m)
    print(f"Using Markov algo, value of the European call option for M = {m} is {price} and time required to compute this is {1000*time_req} milliseconds.")
