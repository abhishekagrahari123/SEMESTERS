import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")


def blackScholes(r, K, T, sigma, t, S):
    if t == T:
        return [max(S - K, 0), max(K - S, 0)]
    d1 = (np.log(S / K) + (r + (sigma**2) / 2) * (T - t)) / (sigma * np.sqrt(T - t))
    d2 = d1 - sigma * np.sqrt(T - t)

    callp = S * norm.cdf(d1, 0, 1) - K * np.exp(-r * (T - t)) * norm.cdf(d2, 0, 1)
    putp = K * np.exp(-r * (T - t)) * norm.cdf(-d2, 0, 1) - S * norm.cdf(-d1, 0, 1)

    return [callp, putp]


T = 1
r = 0.05
sigma = 0.6
S = 1
N = 50
# # Variation with strike price
K = np.linspace(0.1, 2, N)
call_prices = np.zeros(N)
put_prices = np.zeros(N)
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:  # time at which option price is required
    for i in range(N):
        option_price = blackScholes(r, K[i], T, sigma, t, S)
        call_prices[i] = option_price[0]
        put_prices[i] = option_price[1]
    ax1.plot(K, call_prices, label=f't = {t}')
    ax2.plot(K, put_prices, label=f't = {t}')
ax1.set_xlabel('K')
ax1.set_ylabel('Call Price(t)')
ax1.set_title('Call Price(t) vs K')
ax1.legend()
ax2.set_xlabel('K')
ax2.set_ylabel('Put Price(t)')
ax2.set_title('Put Price(t) vs K')
ax2.legend()
fig1.savefig('fig1.png')
fig2.savefig('fig2.png')

r = 0.05
sigma = 0.6
K = 1
S = 1
# Variation with Time to maturity
T = np.linspace(1, 3, N)
call_prices = np.zeros(N)
put_prices = np.zeros(N)
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:  # time at which option price is required
    for i in range(N):
        option_price = blackScholes(r, K, T[i], sigma, t, S)
        call_prices[i] = option_price[0]
        put_prices[i] = option_price[1]
    ax1.plot(T, call_prices, label=f't = {t}')
    ax2.plot(T, put_prices, label=f't = {t}')
ax1.set_xlabel('T')
ax1.set_ylabel('Call Price(t)')
ax1.set_title('Call Price(t) vs T')
ax1.legend()
ax2.set_xlabel('T')
ax2.set_ylabel('Put Price(t)')
ax2.set_title('Put Price(t) vs T')
ax2.legend()
fig1.savefig('fig3.png')
fig2.savefig('fig4.png')

r = 0.05
K = 1
S = 1
T = 1
# Variation with Volatility
sigma = np.linspace(0.1, 0.9, N)
call_prices = np.zeros(N)
put_prices = np.zeros(N)
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:  # time at which option price is required
    for i in range(N):
        option_price = blackScholes(r, K, T, sigma[i], t, S)
        call_prices[i] = option_price[0]
        put_prices[i] = option_price[1]
    ax1.plot(sigma, call_prices, label=f't = {t}')
    ax2.plot(sigma, put_prices, label=f't = {t}')
ax1.set_xlabel('Sigma')
ax1.set_ylabel('Call Price(t)')
ax1.set_title('Call Price(t) vs Sigma')
ax1.legend()
ax2.set_xlabel('Sigma')
ax2.set_ylabel('Put Price(t)')
ax2.set_title('Put Price(t) vs Sigma')
ax2.legend()
fig1.savefig('fig5.png')
fig2.savefig('fig6.png')


K = 1
S = 1
sigma = 0.6
T = 1
# Variation with risk free rate of interest
r = np.linspace(0.05, 1.5, N)
call_prices = np.zeros(N)
put_prices = np.zeros(N)
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:  # time at which option price is required
    for i in range(N):
        option_price = blackScholes(r[i], K, T, sigma, t, S)
        call_prices[i] = option_price[0]
        put_prices[i] = option_price[1]
    ax1.plot(r, call_prices, label=f't = {t}')
    ax2.plot(r, put_prices, label=f't = {t}')
ax1.set_xlabel('Risk Free Return')
ax1.set_ylabel('Call Price(t)')
ax1.set_title('Call Price(t) vs Risk Free Return')
ax1.legend()
ax2.set_xlabel('Risk Free Return')
ax2.set_ylabel('Put Price(t)')
ax2.set_title('Put Price(t) vs Risk Free Return')
ax2.legend()
fig1.savefig('fig7.png')
fig2.savefig('fig8.png')


# 3D PLOTS
N = 20
# VARYING K AND T
T = 1
r = 0.05
sigma = 0.6
S = 1
t = 0
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

K = np.linspace(0.1, 2, N)
T = np.linspace(0.05, 2, N)
K_axis, T_axis = np.meshgrid(K, T)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r, K[i], T[j], sigma, t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(K_axis, T_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('K')
ax1.set_ylabel('T')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying K and T')
ax2.plot_surface(K_axis, T_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('K')
ax2.set_ylabel('T')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying K and T')
fig1.savefig('fig9.png')
fig2.savefig('fig10.png')

# VARYING K AND R
T = 1
sigma = 0.6
S = 1
N = 100
t = 0
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

K = np.linspace(0.1, 2, N)
r = np.linspace(0.01, 2, N)
K_axis, R_axis = np.meshgrid(K, r)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r[j], K[i], T, sigma, t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(K_axis, R_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('K')
ax1.set_ylabel('r')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying K and r')
ax2.plot_surface(K_axis, R_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('K')
ax2.set_ylabel('r')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying K and r')
fig1.savefig('fig11.png')
fig2.savefig('fig12.png')


# # VARYING K AND SIGMA
T = 1
S = 1
t = 0
r = 0.05
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

K = np.linspace(0.1, 2, N)
sigma = np.linspace(0.05, 0.95, N)
K_axis, Sigma_axis = np.meshgrid(K, sigma)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r, K[i], T, sigma[j], t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(K_axis, Sigma_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('K')
ax1.set_ylabel('Sigma')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying K and Sigma')
ax2.plot_surface(K_axis, Sigma_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('K')
ax2.set_ylabel('Sigma')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying K and Sigma')
fig1.savefig('fig13.png')
fig2.savefig('fig14.png')

# # VARYING R AND T
S = 1
t = 0
K = 1
sigma = 0.6
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

r = np.linspace(0.01, 2, N)
T = np.linspace(0.05, 2, N)
R_axis, T_axis = np.meshgrid(r, T)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r[i], K, T[j], sigma, t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(R_axis, T_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('r')
ax1.set_ylabel('T')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying r and T')
ax2.plot_surface(R_axis, T_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('r')
ax2.set_ylabel('R')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying r and T')
fig1.savefig('fig15.png')
fig2.savefig('fig16.png')

# VARYING SIGMA AND T
S = 1
t = 0
K = 1
r = 0.05
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

sigma = np.linspace(0.05, 0.95, N)
T = np.linspace(0.05, 2, N)
Sigma_axis, T_axis = np.meshgrid(sigma, T)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r, K, T[j], sigma[i], t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(Sigma_axis, T_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('Sigma')
ax1.set_ylabel('T')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying Sigma and T')
ax2.plot_surface(Sigma_axis, T_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('Sigma')
ax2.set_ylabel('T')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying Sigma and T')
fig1.savefig('fig17.png')
fig2.savefig('fig18.png')

# VARYING SIGMA AND R
S = 1
t = 0
K = 1
T = 1
fig1, ax1 = plt.subplots(subplot_kw={"projection": "3d"})
fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})

sigma = np.linspace(0.05, 0.95, N)
r = np.linspace(0.01, 2, N)
Sigma_axis, R_axis = np.meshgrid(sigma, r)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r[j], K, T, sigma[i], t, S)
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax1.plot_surface(Sigma_axis, R_axis, callp, cmap='inferno', linewidth=0)
ax1.set_xlabel('Sigma')
ax1.set_ylabel('r')
ax1.set_zlabel('Call Price')
ax1.set_title('Call Price by varying Sigma and r')
ax2.plot_surface(Sigma_axis, R_axis, putp, cmap='inferno', linewidth=0)
ax2.set_xlabel('Sigma')
ax2.set_ylabel('r')
ax2.set_zlabel('Put Price')
ax2.set_title('Put Price by varying Sigma and r')
plt.show()
fig1.savefig('fig19.png')
fig2.savefig('fig20.png')
