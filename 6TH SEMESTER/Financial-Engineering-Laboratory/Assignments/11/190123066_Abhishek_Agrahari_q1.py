import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid')


def yield_calculator(beta, mu, sigma, r0, T):
    if T == 0:
        return r0
    a = beta
    b = beta * mu
    B = (1 / a) * (1 - np.exp(-a * T))
    A = (B - T) * (a * b - (sigma * sigma / 2)) / (a**2) - ((sigma**2) * (B**2)) / (4 * a)
    price = np.exp(A - B * r0)
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
        ax.set_title('Yield Curves using Vasicek Model')
    ax.legend()
    plt.show()


def yield_to_maturity_10_r0(parameters):
    N = 500
    time_to_maturity = np.linspace(0, N, N + 1)
    for para in parameters:
        fig, ax = plt.subplots()
        r0 = np.linspace(0.1, 1, 10)
        for r in r0:
            yield_ = np.zeros(N + 1)
            for i in range(N + 1):
                yield_[i] = yield_calculator(para[0], para[1], para[2], r, time_to_maturity[i])
            ax.plot(time_to_maturity, yield_, label=f'r(0) = {round(r*10)/10}')
        ax.set_xlabel('Time')
        ax.set_ylabel('Yield')
        ax.set_title(f'Yield Curves for [beta, mu, sigma] = [{para[0]}, {para[1]}, {para[2]}]')
        ax.legend()
        plt.show()


para1 = (5.9, 0.2, 0.3, 0.1)
para2 = (3.9, 0.1, 0.3, 0.2)
para3 = (0.1, 0.4, 0.11, 0.1)
parameters = [para1, para2, para3]
yield_to_maturity_single_r0(parameters)
yield_to_maturity_10_r0(parameters)
