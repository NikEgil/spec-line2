import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal

li = list()
for i in range(2):
    li.append(np.zeros((i + 1, 2)))
m = np.array([0.1, 0.2, 0.1, 0.3, 0.5, 0.0, 0.2, 0.8])
ma = np.sort(m)
print(m)
print(ma)
print(np.argsort(np.unique(m), kind="stable"))
print(np.where(m == ma[1])[0][0])
