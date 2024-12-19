import math
from decimal import Decimal,getcontext
import numpy as np

getcontext().prec = 50

def convert(p):
    e = np.e
    T = np.exp(20.3444 * (p**3) + 3) - np.exp(3)
    return T

