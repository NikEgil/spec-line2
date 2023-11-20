import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import statistics as st
from scipy import signal
import re

path_folder = r"C:\Users\Nik\Desktop\prog\data2\15"
path_folder = path_folder.replace(chr(92), "/") + "/"

size = 1  # кол-во графиков
s = 0  # начальный файл
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 450  # нм
end = 650  # нм
step = (884 - 153) / 2134

start_point = round((start - 153) / step)
end_point = start_point + int((end - start) / step)

y = np.zeros(int((end - start) / step))
x = np.arange(start + step, end, step)

alpha = 0.2
n = 0

fig, ax = plt.subplots(figsize=[10, 10])


def car(path_folder, s):
    global n

    for i in range(s, s + size):
        print(s)
        file_list = np.array(os.listdir(path_folder))
        n = len(file_list)
        spec = open(str(path_folder + file_list[i]), "r", encoding="utf8")
        spec = spec.read()
        spec = re.split(",", spec)

        for j in range(start_point, end_point):
            y[j - start_point] = float(spec[j + 11])
        # z = exponential_smoothing(y,alpha)
        #  z = signal.savgol_filter(y, 51, 3)
        plt.plot(x, y, label=file_list[i], color="royalblue", linewidth=1)
        # plt.plot(x, z, label="s " + file_list[i], color="darkorange", linewidth=1)
        # mean = np.mean(z[len(z) - 150 : len(z)])
        # plt.plot(x, z - mean, label="d " + file_list[i], color="green", linewidth=1)

    plt.legend(loc=1, title=round(alpha, 4))
    plt.show()


def exponential_smoothing(series, alpha):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global size
    global alpha
    plt.clf()
    plt.cla()
    if event.key == "right":
        s = s + size
        if s > n - size:
            s = n - size
    if event.key == "left":
        s = s - size
        if s > n - size:
            s = 0
    if event.key == "5":
        s = 100
        for o in range(100):
            car(path_folder, o)
    if event.key == "up":
        size += 1
    if event.key == "down":
        size -= 1
        if size == 0:
            size = 1
    if event.key == "1":
        alpha += 0.002
        print(alpha)
    if event.key == "2":
        alpha -= 0.002
        print(alpha)
    # car(path_folder, s)


fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
