import numpy as np
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt

# Initialise parameters
S0 = 100   #initial stock price
K = 105    #strike price
T = 5     #time to maturity in years
r = 0.05   #annual risk free rate
σ = 0.3

def binomial_tree(N, u, d, q):
    #initialise asset prices at maturity - Time step N
    dt = T/N
    S = np.zeros(N+1)
    S[0] = S0*(d**N)
    for j in range(1,N+1):
        S[j] = S[j-1]*u/d
    
    #initialise option value at maturity
    C = np.zeros(N+1)
    P = np.zeros(N+1)
    for j in range(0,N+1):
        C[j] = max(0,S[j]-K)
        P[j] = max(0,K-S[j])
    
    #step backwards through tree
    for i in np.arange(N,0,-1):
        for j in range(i):
            C[j] = np.exp(-r*dt)*(q*C[j+1] + (1-q)*C[j])
            P[j] = np.exp(-r*dt)*(q*P[j+1] + (1-q)*P[j])
    return C[0],P[0]

M = [1,5,10,20,50,100,200,400]
call_prices = []
put_prices = []

for m in M:
    dt = T/m
    u = np.exp(σ*np.sqrt(dt) + (r-(σ**2)/2)*dt)
    d = np.exp(-σ*np.sqrt(dt) + (r-(σ**2)/2)*dt)
    q = (np.exp(r*dt)-d)/(u-d)  #risk nuetral probability
    if q < 0 or q > 1:
        call_prices.append('-')
        put_prices.append('-')
        continue
    callp, putp = binomial_tree(m,u,d,q)
    call_prices.append(callp)
    put_prices.append(putp)

df = pd.DataFrame({'Step Size':M,'Call Option Price': call_prices, 'Put Option Price': put_prices})
display(df)