# this function generates given no of random numbers from [0,1]
# Xo is the seed
# full period if m is a power of 2, c is odd and a is 4*n + 1
import math
import numpy as np
import statistics
(a, c, m, x) = (2053, 1345, pow(2, 40), 3245)

def Uniform_Distribution():
    global x
    x = (a * x + c) % m 
    return x/m

def Gamma(α, β):
    n = α
    y = 0
    while n > 0:
        u = Uniform_Distribution()
        x = -1*np.log(u)
        y = y + x
        n = n-1
    return y/β

def f(x):
    return np.log(1+x)/x

h = []
for i in range(10000):
    Y = Gamma(2,1.5)
    h.append(f(Y))
μ_cond = np.mean(h)
Variance = statistics.variance(h)

print("Estimated E[h(X,Y)] = ", μ_cond)
print("Estimated variance = ", Variance)