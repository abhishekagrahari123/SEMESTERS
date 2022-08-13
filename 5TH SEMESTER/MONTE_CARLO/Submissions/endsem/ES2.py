import numpy as np
import math
import matplotlib.pyplot as plt
import statistics

# generates random numbers from [0,1]
(a, c, m, x) = (2057, 1345, pow(2, 50), 3245)
def uniform():
    global x
    x = (a * x + c) % m 
    return x/m

# generates normal distribution with mean μ and standard deviation σ
def BoxMuller(μ,σ):
    R = np.sqrt(-2*np.log(uniform()))
    θ = 2*np.pi*uniform()
    return μ + σ*R*np.sin(θ)

P = []
N = 10000
for i in range(10000):
    I = 0
    X = BoxMuller(0,1)
    if X > 4:
        I = 1
    P.append(I)

prob = np.mean(P)/N
var = statistics.variance(P)
std_err = np.sqrt(var/N)
print(f"P(X>4) = {prob}")
print(f"Standard error is {std_err}")
print(f"   CI = [{prob-2.58*np.sqrt(var)},{prob+2.58*np.sqrt(var)}]")

def p(x):
    return (1/math.sqrt(2*math.pi))*math.exp(-0.5*x*x)
def q(x):
    return (1/math.sqrt(2*math.pi))*math.exp(-0.5*(x-4)**2)
def f(x):
    if x > 4:
        return 1
    else:
        return 0

h=np.zeros(N)
for i in range(N):
    X=BoxMuller(4,1)
    h[i]=(f(X)*p(X))/q(X)

μ_imp = np.mean(h)
std_err = np.std(h)/np.sqrt(N)
print(f"μ_imp = ",μ_imp)
print(f"Std Error = ",std_err)
print(f"CI = [{μ_imp-2.58*np.sqrt(np.var(h))},{μ_imp+2.58*np.sqrt(np.var(h))}]")
print(f"Variance = ", std_err*std_err)