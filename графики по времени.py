import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import statistics as st
from scipy import signal
import re
from natsort import natsorted

path_folder = r"c:\Users\Nik\Desktop\prog\только rmr\29"
path_folder = path_folder.replace(chr(92), "/") + "/"

size = 50  # кол-во графиков
s = 0  # начальный файл
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 400  # нм
end = 700  # нм
mean = 650
step = (884 - 153) / 2134

start_point = round((start - 153) / step)
end_point = start_point + int((end - start) / step)
mean_point = round((mean - start) / step)

y = np.zeros(int((end - start) / step))
x = np.arange(start + step, end, step)

alpha = 0.2
n = 0

fig, ax = plt.subplots(figsize=[10, 10])


def car(path_folder, s):
    global n
    a = []
    sp = 0
    ep = len(x)
    file_list = np.array(os.listdir(path_folder))
    file_list = natsorted(file_list)
    for i in range(s, s + size):
        n = len(file_list)

        with open(str(path_folder + file_list[i]), "r", encoding="utf8") as spec:
            spec = spec.read()
            spec = re.split(",", spec)
            for j in range(start_point, end_point):
                y[j - start_point] = float(spec[j + 11])

        # z = exponential_smoothing(y,alpha)
        z = signal.savgol_filter(y, 60, 3)
        a.append(np.max(z) - z[mean_point])
        nx = np.arange(sp, ep, 1)

        plt.subplot(2, 1, 1)
        plt.title(
            "синтез "
            + str(path_folder[-3:-1])
            + " графики "
            + str(s)
            + "-"
            + str(s + size)
        )
        plt.plot(
            nx,
            z,
            # label=file_list[i],
            # color="royalblue",
            alpha=1,
            linewidth=1,
        )
        plt.ylim([-0.01, 0.3])
        # plt.plot(x, z, label="s " + file_list[i], color="darkorange", linewidth=1)
        mean = np.mean(y[len(z) - 300 : len(z)])
        sp += len(x)
        ep += len(x)

    plt.subplot(2, 1, 2)
    plt.title("I(max)-I(650)")
    for i in range(len(a)):
        plt.scatter(i, a[i])
    plt.plot(np.arange(len(a)), a, lw=0.3)
    plt.ylim([0, np.max(a) + 0.01])
    # st = z[len(z) - 50]
    # plt.plot(x, z - st, label="d " + file_list[i], color="green", linewidth=1)

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
    if event.key == "up":
        size += 5
    if event.key == "down":
        size -= 5
        if size < 0:
            size = 1
    if event.key == "1":
        alpha += 0.002
        print(alpha)
    if event.key == "2":
        alpha -= 0.002
        print(alpha)
    car(path_folder, s)


fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
