from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import os
import statistics as st
from scipy import signal
import re

main_folder = r"C:\Users\Nik\Desktop\prog\только rmr"
main_folder = main_folder.replace(chr(92), "/")
print(main_folder)
folders_list = np.array(os.listdir(main_folder), dtype=int)
folders_list = np.sort(folders_list)
print(folders_list)
folders_list = np.array(folders_list, dtype=str)

# region переменные
crit = 0.1
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 400  # нм
end = 700  # нм
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


def get_rmr(spec):
    spec = re.split(",", spec)
    for j in range(start_point, end_point):
        y[j - start_point] = float(spec[j + 11])
    return y


def create():
    li = list()
    for i in range(30):
        li.append(np.zeros((1, len_y)))
    return li


step = 0.01
cmap = cm.get_cmap("winter", 30)
color_list1 = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(30)]
cmap = cm.get_cmap("turbo", 30)
color_list2 = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(30)]


def car(current_folder_path, method, s):
    global n
    file_list = np.array(os.listdir(current_folder_path))
    li = create()
    color = color_list2
    if s == 0:
        color = color_list1
    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        if s == 0:
            mins = np.mean(y[start_mean_point:end_mean_point])
            y -= mins

        if method == 0:
            delta = np.mean(y[start_max_point : start_max_point + 50])
        if method == 1:
            maxs = np.argmax(y)
            delta = np.mean(y[maxs - 50 : maxs + 50])
        if method == 2:
            maxs = np.argmax(y[0 : round(len_y / 2)])
            delta = np.mean(y[maxs - 50 : maxs + 50])
        if method == 3:
            delta = np.max(y)
        for k in range(30):
            if step * k <= delta < step * (k + 1):
                li[k] = np.append(li[k], [y], axis=0)
    k = 0

    for i in range(len(li)):
        a = len(li[i]) - 1
        if a > 0:
            # li[i] = np.sum(li[i], axis=0)
            # li[i] = np.divide(li[i], a)
            # li[i] = signal.savgol_filter(li[i], 60, 3)
            # plt.plot(x, li[i], color=color[i], alpha=0.5, label=a)
            for j in range(len(li[i])):
                # plt.plot(x, li[i], label=str(i) + " " + str(a))
                y = signal.savgol_filter(li[i][j], 60, 3)
                plt.plot(x, y, color=color[i], alpha=0.1)
    plt.ylim(-0.01, 0.3)
    plt.legend(
        title=current_folder_path[-3:] + str(method),
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        borderaxespad=0.0,
    )
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Интенсивность, отн.ед")
    plt.show()


def exponential_smoothing(series, alpha):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


sp = 0


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global sp
    global method
    current_folder_path = main_folder + "/" + folders_list[s] + "/"
    if event.key == "1":
        method += 1
        if method > 3:
            method = 2
    if event.key == "2":
        method -= 1
        if method < 0:
            method = 0
    if event.key == "right":
        s = s + 1

    if event.key == "left":
        s = s - 1

    if event.key == "up":
        sp += 1
        if sp > 2:
            sp = 2

    if event.key == "down":
        sp -= 1
        if sp < 0:
            sp = 0
    if event.key == "5":
        plt.savefig(current_folder_path[-3:] + ".png")
    plt.cla()
    plt.clf()
    if sp == 2:
        car(current_folder_path, method, 1)
        car(current_folder_path, method, 0)
    else:
        car(current_folder_path, method, sp)
    print(s, method)


file_list = []
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
