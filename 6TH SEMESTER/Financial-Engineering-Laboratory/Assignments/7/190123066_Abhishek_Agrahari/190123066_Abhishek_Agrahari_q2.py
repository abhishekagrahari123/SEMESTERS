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


# define variables
T = 1
K = 1
r = 0.05
sigma = 0.6
N = 100

S = np.linspace(0.1, 2, N)  # Stock price at time t
call_prices = np.zeros(N)
put_prices = np.zeros(N)

# 2d plots
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
for t in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:  # time at which option price is required
    for i in range(N):
        option_price = blackScholes(r, K, T, sigma, t, S[i])
        call_prices[i] = option_price[0]
        put_prices[i] = option_price[1]
    ax1.plot(S, call_prices, label=f't = {t}')
    ax2.plot(S, put_prices, label=f't = {t}')
ax1.set_xlabel('S(t)')
ax1.set_ylabel('Call Price(t)')
ax1.set_title('Call Price(t) vs S(t)')
ax1.legend()
ax2.set_xlabel('S(t)')
ax2.set_ylabel('Put Price(t)')
ax2.set_title('Put Price(t) vs S(t)')
ax2.legend()

# 3d plots
N = 20
fig3, ax3 = plt.subplots(subplot_kw={"projection": "3d"})
fig4, ax4 = plt.subplots(subplot_kw={"projection": "3d"})

t = np.linspace(0, 1, N)
S = np.linspace(0.05, 2, N)  # Stock price at time t
t_axis, S_axis = np.meshgrid(t, S)

callp = np.zeros((N, N))
putp = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        option_price = blackScholes(r, K, T, sigma, t[i], S[j])
        callp[i][j] = option_price[0]
        putp[i][j] = option_price[1]

callp = callp.T
putp = putp.T

ax3.scatter3D(S_axis, t_axis, callp, color='r')
ax3.set_xlabel('S(t)')
ax3.set_ylabel('t')
ax3.set_zlabel('Call Price(t)')
ax3.set_title('Call Price(t) by varying t and S(t)')
ax3.view_init(30, -130)  # view_init(elev=None, azim=None)
ax4.scatter(S_axis, t_axis, putp, color='g')
ax4.set_xlabel('S(t)')
ax4.set_ylabel('t')
ax4.set_zlabel('Put Price(t)')
ax4.set_title('Put Price(t) by varying t and S(t)')
plt.show()

# fig1.savefig('fig1.png')
# fig2.savefig('fig2.png')
# fig3.savefig('fig3.png')
# fig4.savefig('fig4.png')
