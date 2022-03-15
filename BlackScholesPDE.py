#Black Scholes PDE skeleton code

import numpy as np
import scipy.sparse
import matplotlib.pyploy as plt
from mlp_toolhits.mplot3d import Axes3D

#Functions for the boundary conditions

def bottom_boundary_condition(K, T, S_min, r, t):
    return np.zeros(t.shape)

def top_boundary_condition(K, T, S_max, r, t):
    return S_max - np.exp(-r*(T-t)) * K

def final_boundary_condition(K, T, S):
    return np.maximum(S-K, 0)

#Functions to calculate the coefficients in Lamda
#Following two functions are derived from algebraic manipulations to the equation with the central difference estimates to isolate each V_i

def compute_abc(K, T, sigma, r, S, dt, dS):
    a = -sigma**2 * S**2/(2* dS**2) + r*S/(2*dS)
    b = r + sigma**2 * S**2/(dS**2)
    c = -sigma**2 * S**2/(2* dS**2) - r*S/(2*dS)
    return a, b, c

def compute_lambda(a, b, c):
    return scipy.sparse.diags( [a[1:], b, c[:-1]], offsets=[-1, 0, 1])

def compute_W(a, b, c, V0, VM):
    M = len(b) + 1
    W = np.zeros(M-1)
    W[0] = a[0] * V0
    W[-1] = c[-1]*VM
    return W


#Combining all this in a function that essentially populates N*M matrix with option values,
#and returns the option value V, the times t, and the stock prices S

def price_call_explicit(K, T, r, sigma, N, M):
    #Choose shape of the grid
    dt = T/N
    S_min = 0
    S_max = K * np.exp(8*sigma*np.sqrt(T))
    dS = (S_max-S_min)/M
    S = np.linspace(S_min, S_max, M+1 )
    t = np.linspace(0, T, N+1)
    V = np.zeros((N+1, M+1))

    #Set the boundary conditions
    V[:,-1] = top_boundary_condition(K, T, S_max, r, t)
    V[:,0] = bottom_boundary_condition(K, T, S_max, r, t)
    V[-1, :] = final_boundary_condition(K, T, S)

    #Apply the recurrence relation
    a, b, c = compute_abc(K, T, sigma, r, S[1:-1], dt, dS)
    Lambda = compute_lambda(a, b, c)
    identity = scipy.sparse.identity(M-1)

    for i in range(N, 0, -1):
        W = compute_W(a, b, c, V[i, 0], V[i, M])
        #Use dot to multiply a vector by a sparse matrix
        V[i-1, 1:M] = (identity-Lamdba*dt).dot(V[i, 1:M]) - W*dt

    return V, t, S

#Find a way to call with actual data, or starting points and plot it in 3D




