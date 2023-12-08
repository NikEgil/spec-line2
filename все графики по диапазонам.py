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

main_folder = r"C:\Users\Nik\Desktop\prog\05-12-23_Setgey_FeO"
base_folder = r"C:\Users\Nik\Desktop\prog\05-12-23_Setgey_FeO\base"
need_base = True
# main_folder = r"C:\Users\Nik\Desktop\prog\Новая папка"
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


def get_rmr(spec):
    spec = re.split(",", spec)
    for j in range(start_point, end_point):
        y[j - start_point] = float(spec[j + 11])
    return y


def get_txt(spec):
    spec = re.split("\n|\t", spec)
    for j in range(start_point, end_point):
        y[j - start_point] = spec[j * 2 + 15].replace(",", ".")
        # print(y[j - start_point])
    return y


def get_csv(spec):
    spec = re.split("\n|,", spec)

    for j in range(start_point, end_point):
        y[j - start_point] = spec[j * 2 + 1].replace(",", ".")
        # print(y[j - start_point])

    return y


def create():
    li = list()
    for i in range(30):
        li.append(np.zeros((1, len_y)))
    return li


step = 0.01
cmap1 = cm.get_cmap("winter")
color_list1 = [
    matplotlib.colors.rgb2hex(cmap1(i)[:3]) for i in range(len(folders_list))
]
cmap2 = cm.get_cmap("turbo")
color_list2 = [
    matplotlib.colors.rgb2hex(cmap2(i)[:3]) for i in range(len(folders_list))
]


def get_base(base_folder):
    b = []
    for a in ("/dark.csv", "/light.csv", "/bg.csv"):
        with open(base_folder + a, "r", encoding="utf8") as spec:
            spec = spec.read()
            b.append(np.copy(get_csv(spec)))
    return b


def calc(mas, d, l, bg):
    pass


def car(current_folder_path, method, s):
    global n
    file_list = np.array(os.listdir(current_folder_path))
    li = np.zeros((0, len_y))
    color = [matplotlib.colors.rgb2hex(cmap2(i)[:3]) for i in range(len(file_list))]
    if s == 0:
        color = [matplotlib.colors.rgb2hex(cmap1(i)[:3]) for i in range(len(file_list))]
    if file_list[0][-1] == "n":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_rmr(spec)
            if s == 0:
                mins = np.mean(y[start_mean_point:end_mean_point])
                y -= mins
            li = np.append(li, [y], axis=0)
    elif file_list[0][-1] == "t":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_txt(spec)
            if s == 0:
                mins = np.mean(y[start_mean_point:end_mean_point])
                y -= mins
            li = np.append(li, [y], axis=0)
    elif file_list[0][-1] == "v":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_csv(spec)
            if s == 0:
                mins = np.mean(y[start_mean_point:end_mean_point])
                y -= mins
            li = np.append(li, [y], axis=0)
    else:
        pass

    if need_base == True:
        a = get_base(base_folder)
        dark, light, bg = a[0], a[1], a[2]
        li = calc(li, dark, light, bg)

    for i in range(len(li)):
        y = signal.savgol_filter(li[i], 60, 3)
        plt.plot(x, y, color=color[i], alpha=0.1)
    # plt.ylim(-0.01, 0.3)

    plt.legend(
        title=current_folder_path[-10:]
        + "\n"
        + str(len(file_list))
        + " "
        + str(len(color)),
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        borderaxespad=0.0,
    )
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Интенсивность, отн.ед")
    plt.show()


sp = 1


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
