import numpy as np
import math

def inverse(time):
    t = np.round(time,4)
    res = np.sqrt((np.log(t+np.exp(3))-3)/20.3444)
    return res

x = inverse(13.9)
print(x)

time_values = np.array([13.9, 14.5, 15.0])
results = inverse(time_values)
print(results)

