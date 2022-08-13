import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

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

   N = 5000
time_step = 1/N

# for calculating E[W(2)] and E[W(5)]
s1 = 0
s2 = 0

# setting plot size
plt.figure(figsize=(11, 8))

# generating W(t) with time step(ti+1- ti) as 1/5000
for i in range(10):
    W = []
    W.append(0)
    for j in range(1,N):
        w = W[j-1] + np.sqrt(time_step)*BoxMuller(0,1)
        W.append(w)
    plt.plot(W)
    
# making the plot
X_ticks = [i*1000 for i in range(6)]
time = [i/5000 for i in X_ticks]
plt.xticks(X_ticks, time)
plt.xlabel('t')
plt.ylabel('W(t)')
plt.title('10 Sample paths for standard Brownian Motion')
plt.show()