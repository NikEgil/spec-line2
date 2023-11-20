import matplotlib.pyplot as plt
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
step_v = (884 - 153) / 2134
start_point = round((start - 153) / step_v)
end_point = start_point + int((end - start) / step_v)

len_y = end_point - start_point
start_mean_point = int(len_y * 0.8)
end_mean_point = int(len_y * 0.9)
y = np.zeros(len_y)
x = np.arange(start + step_v, end, step_v)

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


def create(a):
    li = list()
    for i in range(a):
        li.append(np.zeros((1, len_y)))
    return li


def sm(mas):
    a = len(mas) - 1
    mas = np.sum(mas, axis=0)
    mas = np.divide(mas, a)
    mas = signal.savgol_filter(mas, 60, 3)
    return mas


def cord(mas):
    maxs = np.max(mas) * 0.75
    ind_maxs = np.argmax(mas)
    ind_maxs2 = ind_maxs
    while mas[ind_maxs] > maxs:
        ind_maxs -= 1
    while mas[ind_maxs2] > maxs:
        ind_maxs2 += 1
    ind_maxs = x[ind_maxs]
    ind_maxs2 = x[ind_maxs2]
    return (ind_maxs, ind_maxs2)


step = 0.0125
c1 = round((400 - start) / step_v)
c2 = round((420 - start) / step_v)
print(c1, "aaa", c2, len_y)


def car(current_folder_path, s, method):
    global n
    file_list = np.array(os.listdir(current_folder_path))
    li = np.zeros((len(file_list), len_y))
    mas1 = np.zeros((1, len_y))
    mas2 = np.zeros((1, len_y))
    mas3 = np.zeros((1, len_y))
    delta_m = 0
    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        mins = np.mean(y[start_mean_point:end_mean_point])
        y -= mins
        maxs = np.argmax(y[0 : round(len_y / 2)])
        delta = np.mean(y[maxs - 50 : maxs + 50])
        if delta > delta_m:
            delta_m = delta
        li[file] = y

    for i in range(len(li)):
        delta = np.mean(li[i][maxs - 50 : maxs + 50])
        d = delta_m - delta
        if d <= 0.025:
            mas2 = np.append(mas2, [li[i]], axis=0)

    # lmas1 = len(mas1)
    lmas2 = len(mas2)
    # lmas3 = len(mas3)
    # mas1 = sm(mas1)
    mas2 = sm(mas2)
    #  mas3 = sm(mas3)
    #  label1 = (
    #      "max - 0.0125\n"
    #       + str(round(lmas1))
    #      + "шт"
    #       + str(round(np.argmax(mas1) * step_v + start, 2))
    #       + "нм "
    #       + str(round((np.max(mas1) / np.mean(mas1[c1:c2])), 2))
    #   )
    cor = cord(mas2)
    label2 = (
        "max - 0.025\n"
        + str(round(lmas2))
        + "шт "
        + str(round(np.argmax(mas2) * step_v + start, 2))
        + "нм "
        + str(round((np.max(mas2) / np.mean(mas2[c1:c2])), 2))
        + "\n"
        + str(round(cor[1] - cor[0], 2))
        + "нм "
    )
    # label3 = (
    #   "0.0125 - 0.0375\n"
    #     + str(round(lmas3))
    #     + "шт"
    #     + str(round(np.argmax(mas3) * step_v + start, 2))
    #     + "нм "
    #      + str(round((np.max(mas3) / np.mean(mas3[c1:c2])), 2))
    # )

    print(cor)
    a = np.arange(cor[0], cor[1])
    plt.plot(a, np.ones(len(a)) * np.max(mas2) * 0.75)

    # plt.plot(x, mas1, label=label1)
    plt.plot(x, mas2, label=label2)
    # plt.plot(x, mas3, label=label3)
    plt.legend()
    plt.show()


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global size
    global method
    plt.cla()
    plt.clf()
    if event.key == "1":
        plt.cla()
        plt.clf()
    if event.key == "right":
        s = s + 1

    if event.key == "left":
        s = s - 1

    if event.key == "up":
        method += 1
        if method > 3:
            method = 3
    if event.key == "down":
        method -= 1
        if method < 0:
            method = 0
    print(s, method)
    current_folder_path = main_folder + "/" + folders_list[s] + "/"
    car(current_folder_path, s, method)


file_list = []
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
