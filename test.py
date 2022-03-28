#PDE for American Call Options with Dividend Yield

import numpy as np
import matplotlib.pyplot as plt

N = 252 #number of timesteps
dt = 1/N #time division
sigma = 0.16 #volatity
s_m = 0.226 #max volatity
r = 0.1 #interest rate
q = 0.11 #dividend yield

K = 100 #Strike Price

#Coefficients for PDE
p = (sigma**2) / (2*s_m**2)

mu = r - q - (sigma**2)/2
p_u = p + 0.5* mu * np.sqrt(dt)/(2*s_m)
p_m = 1 - 2*p
p_d = p - 0.5* mu * np.sqrt(dt)/s_m


M = 5 * np.sqrt(N) #Max Option Price Range
Q = int(2 * M + 1)

print("p: %.3f" %(p))
print("P_u: %.3f" %(p_u))
print("P_m: %.3f" %(p_m))
print("P_d: %.3f" %(p_d))
total  = p_d + p_m + p_u
print("Total: %.3f" %(total))
print("M: %d" %(M))
print("K: %d" %(K))
  
#initialize Stock Price, assuming exponential price behavior 
S = np.ones(Q)
S[0] = 100 * np.exp(- M * s_m * np.sqrt(dt))

for i in range(1,Q):
    S[i] = S[i - 1] * np.exp(s_m * np.sqrt(dt))
    
#initialize Call Price Vector
C = np.ones(Q) #American Call
C_e = np.ones(Q) #European Call
for i in range(Q):
    C[i] = max(S[i]-K,0)
    C_e[i] = max(S[i]-K,0)

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(S,C,'.')
ax2.plot(Q,S)

     
for t in range(N): #Iterate Through Time
    for j in range(1,Q - 1): #Iterate Through Stock Price
        C[j] = p_u * C[j+1] + p_m * C[j] + p_d * C[j-1]
        C[j] = C[j] / (1 + r * dt)

        C_e[j] = p_u * C_e[j+1] + p_m * C_e[j] + p_d * C_e[j-1]
        C_e[j] = C_e[j] / (1 + r * dt)


    #Zero Radiation Boundary Conditions
        C[0] = 2* C[1] - C[2]
        C[Q - 1] = 2* C[Q - 2] - C[Q - 3]

        C_e[0] = 2 * C_e[1] - C_e[2]
        C_e[Q - 1] = 2 * C_e[Q - 2] - C_e[Q - 3]
    
    #American Call Option 
    for j in range(Q):
        if C[j] < max(S[j]-K,0):
            C[j] = max(S[j]-K,0) #Ensures the option is >= Stock's intrinsic value
            temp = C[j] - C_e[j]
            print(temp)
            

    if t == 100:
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.plot(S,C,'.',label = "American Call")
        ax2.plot(S,C_e,'.',label = "European Call")
        

plt.show()