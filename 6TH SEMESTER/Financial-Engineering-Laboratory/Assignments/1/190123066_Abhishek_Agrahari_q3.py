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
M = 20
dt = T/M
call_values = np.zeros((M+1,M+1))
put_values = np.zeros((M+1,M+1))

def binomial_tree(u, d, q):
    #initialise asset prices at maturity 
    S = np.zeros(M+1)
    S[0] = S0*(d**M)
    for j in range(1,M+1):
        S[j] = S[j-1]*u/d
    
    #initialise option value at maturity
    C = np.zeros(M+1)
    P = np.zeros(M+1)
    for j in range(0,M+1):
        C[j] = max(0,S[j]-K)
        P[j] = max(0,K-S[j])
    
    #step backwards through tree
    for i in np.arange(M,0,-1):
        call_values[i] = C
        put_values[i] = P
        for j in range(i):
            C[j] = np.exp(-r*dt)*(q*C[j+1] + (1-q)*C[j])
            P[j] = np.exp(-r*dt)*(q*P[j+1] + (1-q)*P[j])
    call_values[0] = C
    put_values[0] = P

u = np.exp(σ*np.sqrt(dt) + (r-(σ**2)/2)*dt)
d = np.exp(-σ*np.sqrt(dt) + (r-(σ**2)/2)*dt)
q = (np.exp(r*dt)-d)/(u-d)  #risk nuetral probability
t = [0,0.50,1,1.50,3,4.5]
if q < 0 or q > 1:
    print("Arbitrage opportunity exists in the model. No risk nuetral measure exists.")
else:
    binomial_tree(u,d,q)
    for time in t:
        i = int(time/dt)
        print(f"For t = {time} (time step = {i}) -")
        df = pd.DataFrame({'No. of up steps': np.arange(i+1), 'No. of down steps': np.arange(i,-1,-1),'Call Option Values': call_values[i][:i+1], 'Put Option Values': put_values[i][:i+1]})
        display(df)    
        print('\n')   
    