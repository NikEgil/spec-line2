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


filename = "output_c.xlsx"
# имя	пик, нм	интентс	ширина,нм	АК	ЦН	ХЗ	ВМ
workbook = load_workbook(filename=filename)
sheet = workbook.active
data = sheet.values
data = np.array(list(data))
name = data[0]
print(name[0])
data = np.delete(data, 0, 0)
data = data.astype(float)


id = data[:, 0]
id = id.astype(int)
peak = data[:, 1]
inten = data[:, 2]
weight = data[:, 3]
v_1 = data[:, 4]
v_2 = data[:, 5]
v_3 = data[:, 6]
v_4 = data[:, 7]
speed = np.zeros(len(v_1))
for i in range(len(speed)):
    speed[i] = v_1[i] + v_2[i] + v_3[i] + v_4[i]


def size(mas):
    return ((mas - np.min(mas)) / (np.max(mas) - np.min(mas)) + 0.1) * 700


def graf(pos, x, y, z, ids, n):
    ax = fig.add_subplot(pos)
    zs = np.sort(z)
    c = 0
    cmap = cm.get_cmap("rainbow", len(np.unique(z)))
    color_list = [
        matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(len(np.unique(z)))
    ]
    print(len(z), len(np.unique(z)), len(color_list))
    for i in range(len(ids)):
        if i == 0 or z[i] != z[i - 1]:
            color = color_list[np.where(z == zs[c])[0][0]]
            c += 1
        ax.scatter(x[i], y[i], color=color, label=ids[i])
        ax.text(x[i], y[i], round(z[i], 2))
        ax.set_xlabel(n[0])
        ax.set_ylabel(n[1])
        ax.set_title(n[2])


fig = plt.figure()
s = 130
print(id)
graf(s + 1, v_1, v_2, peak, id, ("v1", "v2", "положение пика,нм"))
graf(s + 2, v_1, v_2, inten, id, ("v1", "v2", "I(max)/I(min)"))
graf(s + 3, v_1, v_2, weight, id, ("v1", "v2", "ширина,нм"))
if s > 200:
    graf(s + 4, v_1, v_3, peak, id, ("v1", "v3", "положение пика,нм"))
    graf(s + 5, v_1, v_3, inten, id, ("v1", "v3", "I(max)/I(min)"))
    graf(s + 6, v_1, v_3, weight, id, ("v1", "v3", "ширина,нм"))
if s > 300:
    graf(s + 7, v_2, v_3, peak, id, ("v2", "v3", "положение пика,нм"))
    graf(s + 8, v_2, v_3, inten, id, ("v2", "v3", "I(max)/I(min)"))
    graf(s + 9, v_2, v_3, weight, id, ("v2", "v3", "ширина,нм"))
plt.show()
# нижний ряд

fig = plt.figure()
s = 130
no = np.arange(50)
# graf(s + 1, no, no, no, no, ("положение пика,нм", "I(max)/I(min)", "v1"))
graf(s + 1, peak, inten, v_1, id, ("положение пика,нм", "I(max)/I(min)", "v1"))
graf(s + 2, peak, weight, v_1, id, ("положение пика,нм", "ширина,нм", "v1"))
graf(s + 3, weight, inten, v_1, id, ("ширина,нм", "I(max)/I(min)", "v1"))
if s > 200:
    graf(s + 1, peak, inten, v_2, id, ("положение пика,нм", "I(max)/I(min)", "v2"))
    graf(s + 2, peak, weight, v_2, id, ("положение пика,нм", "ширина,нм", "v2"))
    graf(s + 3, weight, inten, v_2, id, ("ширина,нм", "I(max)/I(min)", "v2"))
if s > 300:
    graf(s + 1, peak, inten, v_3, id, ("положение пика,нм", "I(max)/I(min)", "v3"))
    graf(s + 2, peak, weight, v_3, id, ("положение пика,нм", "ширина,нм", "v3"))
    graf(s + 3, weight, inten, v_3, id, ("ширина,нм", "I(max)/I(min)", "v3"))
plt.show()
