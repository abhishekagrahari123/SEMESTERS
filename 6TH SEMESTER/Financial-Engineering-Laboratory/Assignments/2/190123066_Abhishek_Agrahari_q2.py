import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
plt.style.use("seaborn")


def binomial_model(S0, K, r, σ, M):
    # We are using Asian Option as the path dependent derivative
    dt = T / M
    u1 = np.exp(σ * np.sqrt(dt))
    d1 = np.exp(-σ * np.sqrt(dt))
    u2 = np.exp(σ * np.sqrt(dt) + (r - (σ**2) / 2) * dt)
    d2 = np.exp(-σ * np.sqrt(dt) + (r - (σ**2) / 2) * dt)
    q1 = (np.exp(r * dt) - d1) / (u1 - d1)  # risk nuetral probability
    q2 = (np.exp(r * dt) - d2) / (u2 - d2)
    u = [u1, u2]
    d = [d1, d2]
    q = [q1, q2]

    call_prices = []
    put_prices = []

    for t in range(2):
        callOptionPrice, putOptionPrice = 0, 0
        for k in range(0, 2**M):
            price = [S0]
            cnt = 0
            for i in range(0, M):
                val = 0
                if (k & (1 << (i))):
                    cnt += 1
                    val = price[-1] * u[t]
                else:
                    val = price[-1] * d[t]
                price.append(val)
            Savg = np.mean(price)
            callPayoff = max(Savg - K, 0)
            putPayoff = max(K - Savg, 0)
            callOptionPrice += (q[t]**cnt) * ((1 - q[t])**(M - cnt)) * callPayoff
            putOptionPrice += (q[t]**cnt) * ((1 - q[t])**(M - cnt)) * putPayoff

        callOptionPrice /= np.exp(r * T)
        putOptionPrice /= np.exp(r * T)
        call_prices.append(callOptionPrice)
        put_prices.append(putOptionPrice)
    return call_prices[0], put_prices[0], call_prices[1], put_prices[1]


def plot_2d():
    for i in range(4):
        fig1, ax1 = plt.subplots()
        fig2, ax2 = plt.subplots()
        ax1.plot(A[i], call2d[i][0], label='Call Prices')
        ax1.plot(A[i], put2d[i][0], label='Put Prices')
        ax2.plot(A[i], call2d[i][1], label='Call Prices')
        ax2.plot(A[i], put2d[i][1], label='Put Prices')
        ax1.legend()
        ax2.legend()
        ax1.set_title(f'Asian Option Price vs {x_label[i]} (Set 1 of u,d)')
        ax1.set_xlabel(f'{x_label[i]}')
        ax1.set_ylabel('Asian Option Price')
        ax2.set_title(f'Option Price vs {x_label[i]} (Set 2 of u,d)')
        ax2.set_xlabel(f'{x_label[i]}')
        ax2.set_ylabel('Asian Option Price')


def plot_3d():
    for i in range(4):
        for j in range(i + 1, 4):
            fig1 = plt.figure(figsize=(8, 8))
            fig2 = plt.figure(figsize=(8, 8))
            fig3 = plt.figure(figsize=(8, 8))
            fig4 = plt.figure(figsize=(8, 8))
            ax1 = fig1.add_subplot(111, projection='3d')
            ax2 = fig2.add_subplot(111, projection='3d')
            ax3 = fig3.add_subplot(111, projection='3d')
            ax4 = fig4.add_subplot(111, projection='3d')

            ax1.scatter(np.tile(A[i], N), np.tile(A[j], N), call3d[i][j][0].ravel(), label='Call Prices')
            ax2.scatter(np.tile(A[i], N), np.tile(A[j], N), put3d[i][j][0].ravel(), label='Put Prices')
            ax3.scatter(np.tile(A[i], N), np.tile(A[j], N), call3d[i][j][1].ravel(), label='Call Prices')
            ax4.scatter(np.tile(A[i], N), np.tile(A[j], N), put3d[i][j][1].ravel(), label='Put Prices')

            ax1.set_title(f'Call Price vs ({x_label[i]} and {x_label[j]}) (Set 1 of u,d)')
            ax1.set_xlabel(f'{x_label[i]}')
            ax1.set_ylabel(f'{x_label[j]}')
            ax1.set_zlabel('Call Price')

            ax2.set_title(f'Put Price vs ({x_label[i]} and {x_label[j]}) (Set 1 of u,d)')
            ax2.set_xlabel(f'{x_label[i]}')
            ax2.set_ylabel(f'{x_label[j]}')
            ax2.set_zlabel('Put Price')

            ax3.set_title(f'Call Price vs ({x_label[i]} and {x_label[j]}) (Set 2 of u,d)')
            ax3.set_xlabel(f'{x_label[i]}')
            ax3.set_ylabel(f'{x_label[j]}')
            ax3.set_zlabel('Call Price')

            ax4.set_title(f'Put Price vs ({x_label[i]} and {x_label[j]}) (Set 2 of u,d)')
            ax4.set_xlabel(f'{x_label[i]}')
            ax4.set_ylabel(f'{x_label[j]}')
            ax4.set_zlabel('Put Price')


# Initialise parameters
S0 = 100  # initial stock price
K = 100  # strike price
T = 1  # time to maturity in years
r = 0.08  # annual risk free rate
σ = 0.2
M = 10

# Senstivity analysis
left = [50, 50, 0.06, 0.05]
right = [150, 150, 0.7, 0.35]
N = 20
x_label = ['Initial Stock Price', 'Strike Price', 'Risk Free Rate', 'Volatility', 'No of steps']
A = np.zeros((4, N))
for i in range(4):
    A[i] = np.linspace(left[i], right[i], N)

call2d = np.zeros((4, 2, N))
put2d = np.zeros((4, 2, N))
call3d = np.zeros((4, 4, 2, N, N))
put3d = np.zeros((4, 4, 2, N, N))

for j in np.arange(N):
    call2d[0][0][j], put2d[0][0][j], call2d[0][1][j], put2d[0][1][j] = binomial_model(A[0][j], K, r, σ, M)
    call2d[1][0][j], put2d[1][0][j], call2d[1][1][j], put2d[1][1][j] = binomial_model(S0, A[1][j], r, σ, M)
    call2d[2][0][j], put2d[2][0][j], call2d[2][1][j], put2d[0][1][j] = binomial_model(S0, K, A[2][j], σ, M)
    call2d[3][0][j], put2d[3][0][j], call2d[3][1][j], put2d[3][1][j] = binomial_model(S0, K, r, A[3][j], M)

for i in range(N):
    for j in np.arange(N):
        call3d[0][1][0][i][j], put3d[0][1][0][i][j], call3d[0][1][1][i][j], put3d[0][1][1][i][j] = binomial_model(A[0][i], A[1][j], r, σ, M)
        call3d[0][2][0][i][j], put3d[0][2][0][i][j], call3d[0][2][1][i][j], put3d[0][2][1][i][j] = binomial_model(A[0][i], K, A[2][j], σ, M)
        call3d[0][3][0][i][j], put3d[0][3][0][i][j], call3d[0][3][1][i][j], put3d[0][3][1][i][j] = binomial_model(A[0][i], K, r, A[3][j], M)
        call3d[1][2][0][i][j], put3d[1][2][0][i][j], call3d[1][2][1][i][j], put3d[1][2][1][i][j] = binomial_model(S0, A[1][i], A[2][j], σ, M)
        call3d[1][3][0][i][j], put3d[1][3][0][i][j], call3d[1][3][1][i][j], put3d[1][3][1][i][j] = binomial_model(S0, A[1][i], r, A[3][j], M)
        call3d[2][3][0][i][j], put3d[2][3][0][i][j], call3d[2][3][1][i][j], put3d[2][3][1][i][j] = binomial_model(S0, K, A[2][i], A[3][j], M)


plot_2d()
plot_3d()
plt.tight_layout()
plt.show()
