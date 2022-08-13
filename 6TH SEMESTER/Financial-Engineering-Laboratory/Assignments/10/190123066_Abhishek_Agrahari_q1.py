import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


def stock_price_generator(N, S0, T, sig, rate):
    dt = T / N
    s = np.zeros(N + 1)
    s[0] = S0
    for i in range(1, N + 1):
        s[i] = s[i - 1] * np.exp(sig * np.sqrt(dt) * np.random.normal(0, 1) + (rate - sig * sig / 2) * dt)
    return s


def graph_plotter(ax, X, Y, title, xlabel, ylabel):
    ax.plot(X, Y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def stock_plotter(N, S0, T, sig, r, mu):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for i in range(10):
        s = stock_price_generator(N, S0, T, sig, mu)
        srn = stock_price_generator(N, S0, T, sig, r)
        graph_plotter(ax[0], np.linspace(0, T, N + 1), s, '10 GBMs in real world', 'Time (in years)', 'Asset Price (S(t))')
        graph_plotter(ax[1], np.linspace(0, T, N + 1), srn, '10 GBMs in risk nuetral world', 'Time (in years)', 'Asset Price (S(t))')
    plt.show()


def asian_option_price_calculator(N, S0, T, sig, r, K, optionType):
    n = 50
    payoff_sum = 0
    for i in range(n):
        s = stock_price_generator(N, S0, T, sig, r)
        if(optionType == 'Call'):
            payoff_sum = payoff_sum + max(0, np.mean(s) - K)
        else:
            payoff_sum = payoff_sum + max(0, K - np.mean(s))
    price = np.exp(-r * T) * payoff_sum / n
    return price


def optionPriceSensitivityAnalysis(N, S0, T, Sig, R, K, optionType):
    n = 50
    op_k = np.zeros(n)
    op_r = np.zeros(n)
    op_sig = np.zeros(n)
    op_t = np.zeros(n)

    k_array = np.linspace(60, 140, n)
    r_array = np.linspace(0.01, 1, n)
    sig_array = np.linspace(0.01, 1, n)
    t_array = np.linspace(0.01, 5, n)

    fig, ax = plt.subplots(2, 2, figsize=(10, 10))
    ax = ax.flatten()
    for idx, k in enumerate(k_array):
        op_k[idx] = asian_option_price_calculator(N, S0, T, Sig, R, k, optionType)
    graph_plotter(ax[0], k_array, op_k, '', 'K', f'{optionType} price')

    for idx, r in enumerate(r_array):
        op_r[idx] = asian_option_price_calculator(N, S0, T, Sig, r, K, optionType)
    graph_plotter(ax[1], r_array, op_r, '', 'Risk Free Rate', f'{optionType} price')

    for idx, sig in enumerate(sig_array):
        op_sig[idx] = asian_option_price_calculator(N, S0, T, sig, R, K, optionType)
    graph_plotter(ax[2], sig_array, op_sig, '', 'Volatility', f'{optionType} price')

    for idx, t in enumerate(t_array):
        op_t[idx] = asian_option_price_calculator(N, S0, t, Sig, R, K, optionType)
    graph_plotter(ax[3], t_array, op_t, '', 'Time to Maturity (in years)', f'{optionType} price')
    fig.suptitle(f'{optionType} Option Price Sensitivity Analysis')
    plt.show()


N = 100
S0 = 100
T = 0.5
sig = 0.2
r = 0.05
mu = 0.1
stock_plotter(N, S0, T, sig, r, mu)
print(f'Call option price with K = 90 is {asian_option_price_calculator(N, S0, T, sig, r, 90, "Call")}')
print(f'Call option price with K = 105 is {asian_option_price_calculator(N, S0, T, sig, r, 105, "Call")}')
print(f'Call option price with K = 110 is {asian_option_price_calculator(N, S0, T, sig, r, 110, "Call")}')
print(f'Put option price with K = 90 is {asian_option_price_calculator(N, S0, T, sig, r, 90, "Put")}')
print(f'Put option price with K = 105 is {asian_option_price_calculator(N, S0, T, sig, r, 105, "Put")}')
print(f'Put option price with K = 110 is {asian_option_price_calculator(N, S0, T, sig, r, 110, "Put")}')
optionPriceSensitivityAnalysis(N, S0, T, r, sig, 105, 'Call')
optionPriceSensitivityAnalysis(N, S0, T, r, sig, 105, 'Put')
