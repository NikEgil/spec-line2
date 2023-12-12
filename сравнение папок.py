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

main_folder1 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-1"
main_folder2 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-2"
main_folder3 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-3"
base_folder1 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-1\base"
base_folder2 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-2\base"
base_folder3 = r"C:\Users\Nik\Desktop\prog\08-12-2023_Zagrebaev_Au_NPs\T=20\1-3\base"
need_base = True


folders_list = np.array(os.listdir(main_folder1))

print(folders_list)
# folders_list = np.array(folders_list, dtype=str)

# region переменные
crit = 0.1
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 350  # нм
end = 750  # нм
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
cmap2 = cm.get_cmap("turbo")


def get_base(base_folder):
    b = []
    for a in ("/dark.csv", "/light.csv", "/bg.csv"):
        with open(base_folder + a, "r", encoding="utf8") as spec:
            spec = spec.read()
            b.append(np.copy(get_csv(spec)))
    return b


base1 = get_base(base_folder1)
base2 = get_base(base_folder2)
base3 = get_base(base_folder3)


def calc(mas, base):
    d = base[0]
    l = base[1]
    bg = base[2]
    lbg = l - bg
    m = np.copy(mas)
    for i in range(len(m)):
        a = m[i] - bg
        b = a / lbg
        c = np.log10(b)
        m[i] = -c
    return m


li = np.zeros((0, len_y))


def car(current_folder_path, base):
    global li
    file_list = np.array(os.listdir(current_folder_path))
    li = np.zeros((0, len_y))
    if file_list[0][-1] == "n":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_rmr(spec)
            li = np.append(li, [y], axis=0)
    elif file_list[0][-1] == "t":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_txt(spec)
            li = np.append(li, [y], axis=0)
    elif file_list[0][-1] == "v":
        for file in range(len(file_list)):
            with open(
                current_folder_path + file_list[file], "r", encoding="utf8"
            ) as spec:
                spec = spec.read()
                y = get_csv(spec)
            li = np.append(li, [y], axis=0)
    else:
        pass

    if need_base == True:
        li = calc(li, base)


def ploter(mas, color, tex, sm):
    a = 0
    if sm == 1:
        for i in range(len(mas)):
            spec = signal.savgol_filter(mas[i], 60, 3)
            if mas[i][400] > 0.05:
                plt.plot(x, spec, color=color, alpha=0.2)
                if a == 0:
                    plt.plot(
                        x,
                        spec,
                        color=color,
                        alpha=0.2,
                        label=tex[-15:],
                    )
                    a += 1
    else:
        for i in range(len(mas)):
            if mas[i][400] > 0.05:
                plt.plot(x, mas[i], color=color, alpha=0.2)
                if a == 0:
                    plt.plot(
                        x,
                        mas[i],
                        color=color,
                        alpha=0.2,
                        label=tex[-15:],
                    )
                    a += 1

    plt.legend(
        title=tex[-15:],
        bbox_to_anchor=(1.01, 1),
        loc="upper left",
        borderaxespad=0.0,
    )
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Интенсивность, отн.ед")
    plt.show()


sm = 0


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global sm

    if event.key == "right":
        s = s + 1
    if event.key == "left":
        s = s - 1
    if event.key == "up":
        sm = sm + 1
    if event.key == "down":
        sm = sm - 1
    current_folder_path1 = main_folder1 + "/" + folders_list[s] + "/"
    current_folder_path2 = main_folder2 + "/" + folders_list[s] + "/"
    current_folder_path3 = main_folder3 + "/" + folders_list[s] + "/"
    plt.cla()
    plt.clf()
    car(current_folder_path1, base1)
    ploter(li, "red", current_folder_path1, sm)
    car(current_folder_path2, base2)
    ploter(li, "blue", current_folder_path2, sm)
    car(current_folder_path3, base3)
    ploter(li, "green", current_folder_path3, sm)
    print(s, method)


file_list = []
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
