from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import os
import statistics as st
from scipy import signal
import re
from openpyxl import Workbook
from pylab import *
from openpyxl import load_workbook

# main_folder = r"C:\Users\Nik\Desktop\prog\только rmr"
main_folder = r"C:\Users\Nik\Desktop\prog\05-12-23_Setgey_FeO"
base_folder = r"C:\Users\Nik\Desktop\prog\05-12-23_Setgey_FeO\base"
main_folder = main_folder.replace(chr(92), "/")
print(main_folder)
folders_list = np.array(os.listdir(main_folder))
folders_list = np.sort(folders_list)
print(folders_list)
folders_list = np.array(folders_list, dtype=str)

# region переменные
crit = 0.1
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 300  # нм
end = 800  # нм
step = (884 - 153) / 2134
start_point = round((start - 153) / step)
end_point = start_point + int((end - start) / step)

len_y = end_point - start_point
start_mean_point = int(len_y * 0.8)
end_mean_point = int(len_y * 0.9)
y = np.zeros(len_y)
x = np.arange(start + step, end, step)

start_max_point = round(len_y * 0.27)
print(start_max_point, len_y)
# endregion
method = 0
s = 0  # начальная папка

fig, ax = plt.subplots(figsize=[10, 10])


def get_csv(spec):
    spec = re.split("\n|,", spec)

    for j in range(start_point, end_point):
        y[j - start_point] = spec[j * 2 + 1].replace(",", ".")
        # print(y[j - start_point])

    return y


def get_base(base_folder):
    b = []
    for a in ("/dark.csv", "/light.csv", "/bg.csv"):
        with open(base_folder + a, "r", encoding="utf8") as spec:
            spec = spec.read()
            b.append(np.copy(get_csv(spec)))
    return b


a = get_base(base_folder)
dark, light, bg = a[0], a[1], a[2]
plt.plot(x, bg, color="red", label="bg")
plt.plot(x, light, color="blue", label="light")
plt.plot(x, dark, color="gray", label="dark")
plt.legend()
print("dark")
print(dark[150:160])
print("light")
print(light[150:160])
print()
plt.show()
