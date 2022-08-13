import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid')


def B(a, b, gamma, sigma, x):
    B = (2 * (np.exp(gamma * x) - 1)) / ((gamma + a) * (np.exp(gamma * x) - 1) + 2 * gamma)
    return B


def A0(a, b, gamma, sigma, x):
    A0_ = ((2 * gamma * np.exp((a + gamma) * x / 2)) / ((gamma + a) * (np.exp(gamma * x) - 1) + 2 * gamma))**(2 * a * b / (sigma**2))
    return A0_


def yield_calculator(beta, mu, sigma, r0, T):
    if T == 0:
        return r0
    a = beta
    b = mu
    gamma = np.sqrt(a**2 + 2 * sigma**2)
    A0_ = A0(a, b, gamma, sigma, T)
    B_ = B(a, b, gamma, sigma, T)
    price = A0_ * np.exp(-B_ * r0)
    yield_ = -np.log(price) / T
    return yield_


def yield_to_maturity_single_r0(parameters):
    N = 10
    time_to_maturity = np.linspace(0, N, N + 1)
    fig, ax = plt.subplots()
    for para in parameters:
        yield_ = np.zeros(N + 1)
        for i in range(N + 1):
            yield_[i] = yield_calculator(para[0], para[1], para[2], para[3], time_to_maturity[i])
        ax.plot(time_to_maturity, yield_, label=f'[{para[0]}, {para[1]}, {para[2]}, {para[3]}]')
        ax.set_xlabel('Time')
        ax.set_ylabel('Yield')
        ax.set_title('Yield Curves using CIR Model')
    ax.legend()
    plt.show()


def yield_to_maturity_10_r0(para):
    N = 600
    time_to_maturity = np.linspace(0, N, N + 1)
    fig, ax = plt.subplots()
    r0 = np.linspace(0.1, 1, 10)
    for r in r0:
        yield_ = np.zeros(N + 1)
        for i in range(N + 1):
            yield_[i] = yield_calculator(para[0], para[1], para[2], r, time_to_maturity[i])
        ax.plot(time_to_maturity, yield_, label=f'r(0) = {round(r*10)/10}')
    ax.set_xlabel('Time')
    ax.set_ylabel('Yield')
    ax.set_title(f'Yield Curves using CIR model for [beta, mu, sigma] = [{para[0]}, {para[1]}, {para[2]}]')
    ax.legend()
    plt.show()


para1 = (0.02, 0.7, 0.02, 0.1)
para2 = (0.7, 0.1, 0.3, 0.2)
para3 = (0.06, 0.09, 0.5, 0.02)
parameters = [para1, para2, para3]
yield_to_maturity_single_r0(parameters)
yield_to_maturity_10_r0(para1)
