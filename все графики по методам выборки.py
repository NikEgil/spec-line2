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
folders_list = np.array(os.listdir(main_folder))


# region переменные
crit = 0.1
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 400  # нм
end = 700  # нм
mean = 650
min = 420
lamp = 565
step = (884 - 153) / 2134
start_point = round((start - 153) / step)
end_point = start_point + int((end - start) / step)

len_y = end_point - start_point
lamp_point = round((lamp - start) / step)
mean_point = round((mean - start) / step)
min_point = round((min - start) / step)
y = np.zeros(len_y)
x = np.arange(start + step, end, step)

start_max_point = round(len_y * 0.27)
print(start_max_point, len_y)
# endregion

s = 0  # начальная папка
mas = 0
li = 0
lis = 0
fig, ax = plt.subplots(figsize=[10, 10])
reg = 0.015


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


def printer(mas, color, name, alpha):
    for i in range(len(mas)):
        if i == 0:
            plt.plot(
                x,
                mas[i],
                color=color,
                alpha=alpha,
                label=name[-3:] + "метод " + str(len(mas)) + "шт",
            )
        else:
            plt.plot(
                x,
                mas[i],
                color=color,
                alpha=alpha,
            )

    plt.ylim(-0.01, 0.4)
    plt.legend(
        #  bbox_to_anchor=(1.01, 1),
        loc="upper right",
        borderaxespad=0.0,
    )
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Интенсивность, отн.ед")
    plt.show()


def car(current_folder_path, s):
    global mas
    file_list = np.array(os.listdir(current_folder_path))
    mas = np.zeros((len(file_list), len(x)))
    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        mas[file] = signal.savgol_filter(y, 60, 3)

    print(len(mas))


def m1(mas):
    global li
    li = np.zeros((0, len_y))
    maxs = 0
    for i in range(len(mas)):
        delta = np.max(mas[i])
        if delta > maxs:
            maxs = delta
    maxs = maxs - reg
    for i in range(len(mas)):
        if np.max(mas[i]) >= maxs:
            li = np.append(li, [mas[i]], axis=0)
    printer(li, "red", "1", 0.2)


def m2(mas):
    global li
    li = np.zeros((0, len_y))
    m = np.copy(mas)
    delta = 0
    for i in range(len(m)):
        mins = np.max(m[i]) - m[i][mean_point]
        if mins > delta:
            delta = mins
    delta -= reg
    for i in range(len(m)):
        mins = np.max(m[i]) - m[i][mean_point]
        if mins > delta:
            li = np.append(li, [m[i]], axis=0)
    printer(li, "green", "2", 0.2)


def m3(mas):
    global li
    li = np.zeros((0, len_y))
    maxs = 0
    m = np.copy(mas)
    for i in range(len(mas)):
        mins = mas[i][mean_point]
        m[i] -= mins
    for i in range(len(m)):
        delta = np.max(m[i])
        if delta > maxs:
            maxs = delta
    maxs = maxs - reg

    for i in range(len(m)):
        if np.max(m[i]) >= maxs:
            li = np.append(li, [m[i]], axis=0)
    # printer(li, "blue", "3", 0.2)


def sm(ar):
    global lis
    lis = np.zeros(len_y)
    a = len(ar)
    lis = np.sum(ar, axis=0)
    lis /= a

    plt.plot(
        x,
        lis,
        color="black",
        alpha=1,
    )


def peak(ar):
    maxs = np.max(ar)
    y1 = np.arange(0, maxs, 0.001)
    i1 = ar[min_point]
    imax = x[np.argmax(ar)]
    intens = np.max(ar) / i1
    ind3 = int(imax)
    ylam = ar[lamp_point]
    y2 = np.arange(0, ylam, 0.001)
    while ar[ind3] > i1:
        ind3 += 1
        print(ind3)
    plt.plot(
        np.ones(len(y1)) * imax,
        y1,
        color="gray",
        alpha=1,
        label="пик:" + str(round(ind3, 2)) + "нм " + "инт:" + str(round(intens, 2)),
    )
    # plt.plot(
    #      np.ones(len(y2)) * x[lamp_point],
    #      y2,
    ##      color="red",
    #     alpha=1,
    #     label="пик:" + str(round(ind3, 2)) + "нм " + "инт:" + str(round(intens, 2)),
    # )
    plt.legend(loc="upper right", borderaxespad=0.0)


sp = 0
current_folder_path = main_folder + "/" + folders_list[0] + "/"


def up(a):
    return main_folder + "/" + folders_list[a] + "/"


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global mas
    global current_folder_path
    if event.key == "1":
        m1(mas)
        print("method 1")
    if event.key == "2":
        m2(mas)
        print("method 2")
    if event.key == "3":
        m3(mas)
        print("method 3")
    if event.key == "right":
        s = s + 1
        print("open " + up(s))

        car(up(s), sp)
    if event.key == "left":
        s = s - 1
        print("open " + up(s))
        plt.title(label=str(folders_list[s]))
        car(up(s), sp)
    if event.key == "0":
        plt.cla()
        plt.clf()
    if event.key == "4":
        sm(li)
    if event.key == "5":
        peak(lis)
    if event.key == "8":
        plt.savefig(current_folder_path[-3:])
    plt.title(label=str(folders_list[s]))
    plt.show()


file_list = []
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
