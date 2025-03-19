import numpy as np

'''
The real-valued reward function
'''
def f(x, y):
    return np.cos(x/3) + np.cos(y/3) - pow(x/15,2) - pow(y/15,2)