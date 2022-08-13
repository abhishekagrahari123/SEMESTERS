import numpy as np


def stock_price_generator(N, S0, T, sig, rate):
    dt = T / N
    sp = np.zeros(N + 1)
    sn = np.zeros(N + 1)
    sp[0] = S0
    sn[0] = S0
    for i in range(1, N + 1):
        dw = np.random.normal(0, 1)
        sp[i] = sp[i - 1] + sp[i - 1] * (sig * np.sqrt(dt) * dw + rate * dt)
        sn[i] = sn[i - 1] + sn[i - 1] * (sig * np.sqrt(dt) * (-dw) + rate * dt)
    return sp, sn


def asian_option_price_calculator(N, S0, T, sig, r, K, optionType):
    n = 100
    payoff_sum_red = 0
    payoff_sum = 0
    for i in range(n):
        sp, sn = stock_price_generator(N, S0, T, r, sig)
        if(optionType == 'Call'):
            payoff_sum += max(0, np.mean(sp) - K)
            payoff = 0.5 * (max(0, np.mean(sp) - K) + max(0, np.mean(sn) - K))
            payoff_sum_red += payoff
        else:
            payoff_sum = payoff_sum + max(0, K - np.mean(sp))
            payoff = 0.5 * (max(0, K - np.mean(sp)) + max(0, K - np.mean(sn)))
            payoff_sum_red = payoff_sum_red + payoff
    price_red = np.exp(-r * T) * payoff_sum_red / n
    price = np.exp(-r * T) * payoff_sum / n
    return price_red, price


def variance_comparison(N, S0, T, sig, r, K, optionType):
    n = 50
    with_var_red = np.zeros(n)
    without_var_red = np.zeros(n)
    for i in range(n):
        with_var_red[i], without_var_red[i] = asian_option_price_calculator(N, S0, T, sig, r, K, optionType)
    print(f'Variance of {optionType} price for K = {K} with and without variance reduction is ({np.round(np.var(with_var_red), 7)}, {np.round(np.var(without_var_red), 7)})')


N = 100
S0 = 100
T = 0.5
sig = 0.2
r = 0.05
mu = 0.1
K = 105

print(f'Call price for K = 90 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 90, "Call")}')
print(f'Call price for K = 105 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 105, "Call")}')
print(f'Call price for K = 110 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 110, "Call")}')
print(f'Put price for K = 90 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 90, "Put")}')
print(f'Put price for K = 105 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 105, "Put")}')
print(f'Put price for K = 110 with and without variance reduction is {asian_option_price_calculator(N, S0, T, sig, r, 110, "Put")}')
variance_comparison(N, S0, T, sig, r, 90, 'Call')
variance_comparison(N, S0, T, sig, r, 105, 'Call')
variance_comparison(N, S0, T, sig, r, 110, 'Call')
variance_comparison(N, S0, T, sig, r, 90, 'Put')
variance_comparison(N, S0, T, sig, r, 105, 'Put')
variance_comparison(N, S0, T, sig, r, 110, 'Put')
