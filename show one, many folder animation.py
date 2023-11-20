import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from scipy import signal
import time
import re
from pylab import *


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
print("len y ", len_y)
start_mean_point = int(len_y * 0.8)
end_mean_point = int(len_y * 0.9)
print(start_mean_point, end_mean_point)
y = np.zeros(len_y)

x = np.arange(start + step, end, step)
# endregion


def get_rmr(spec):
    spec = re.split(",", spec)
    for j in range(start_point, end_point):
        y[j - start_point] = float(spec[j + 11])
    return y


def get_txt(spec):
    spec = re.split("\n|\t", spec)
    k = len(y)
    for j in range(start_point, end_point):
        y[j - start_point] = spec[j * 2 + 15].replace(",", ".")
        # print(y[j - start_point])
    return y


n = 0


def ploting(a, b, t):
    ax.cla()

    b = signal.savgol_filter(b, 50, 3)

    ax.plot(
        a,
        b,
        linewidth=1.5,
        alpha=1,
        label=t
        # color=[  0.2,4 / 1 / (len(ax.get_lines()) + 5),1 - 1 / (len(ax.get_lines()) + 1),],
    )
    ax.legend()
    plt.ylim([-0.01, 0.2])
    fig.canvas.draw()
    fig.canvas.flush_events()


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

start_time = time.time()
a = 0
mas = np.zeros((1, len(x)))
for folder in range(len(folders_list)):
    current_folder_path = main_folder + "/" + folders_list[folder] + "/"
    current_folder = folders_list[folder]
    print(current_folder_path)
    file_list = np.array(os.listdir(current_folder_path))
    print("graphs ", len(file_list))

    crit = 0.0
    color_step = 1 / len(folders_list)
    q = 0
    t = folders_list[folder]
    if file_list[0][-1] == "n":
        for file in range(len(file_list)):
            spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
            spec = spec.read()
            y = get_rmr(spec)
            z = y - np.mean(y[start_mean_point:end_mean_point])

            if np.max(z) > crit:
                ploting(x, z, t)
                q += 1
            if q > 100:
                break

    elif file_list[0][-1] == "t":
        for file in range(len(file_list)):
            spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
            spec = spec.read()
            y = get_txt(spec)

            z = y - np.mean(y[start_mean_point:end_mean_point])
            if np.max(z) > crit:
                ploting(x, z, t)
                q += 1
            if q > 100:
                break
    if q > 100:
        continue


print("Elapsed time: ", time.time() - start_time)

plt.ioff()
plt.show()
