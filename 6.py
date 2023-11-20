import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal

li = list()
for i in range(2):
    li.append(np.zeros((i + 1, 2)))

a = np.array([5, 5])
li[1] = np.append(li[1], [a], axis=0)
li[1] = np.append(li[1], [a * 2], axis=0)

print(li[1])

print(len(li), len(li[1]))
