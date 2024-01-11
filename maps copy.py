import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from scipy import signal
import time
import re
from openpyxl import Workbook
from pylab import *
from openpyxl import load_workbook
import pandas as pd


data = pd.read_csv("0.27 v АК  интентс.csv")
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

x = data["v1"][:200].to_numpy()
y = []
for i in range(200):
    y.append(data["v2"].loc[i * 200])

x, y = np.meshgrid(x, y)
z = np.zeros((200, 200))
for i in range(200):
    for j in range(200):
        z[i][j] = data["v3"].loc[i * 200 + j]

ax.plot_surface(x, y, z, cmap="viridis")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.show()
