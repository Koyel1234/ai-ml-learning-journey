import numpy as np

class ActivationFunctions:
    
    def linear(x):
        return x

    def step(x):
        return 1 if x>=0 else 0

    def sigmoid(x):
        return 1/(1 + np.exp(-x))

    def tanh(x):
        return ((np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x)))
        