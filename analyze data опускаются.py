import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from scipy import signal
import time
import re
from openpyxl import Workbook
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
start_mean_point = int(len_y * 0.8)
end_mean_point = int(len_y * 0.9)
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


def sm(mas):
    a = len(mas)
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


c1 = round((400 - start) / step)
c2 = round((420 - start) / step)
mean_point = round((650 - start) / step)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
cmap = cm.get_cmap("jet", len(folders_list))
color_list = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(len(folders_list))]

start_time = time.time()

data = np.zeros((len(folders_list) + 1, 4), dtype="object")
data[0] = ["имя", "пик, нм", "интентс", "ширина"]
# len(folders_list)
p = 1
for folder in range(len(folders_list)):
    current_folder_path = main_folder + "/" + folders_list[folder] + "/"
    current_folder = folders_list[folder]
    file_list = np.array(os.listdir(current_folder_path))

    print("in " + current_folder + " graphs ", len(file_list))
    mas = np.zeros((len(file_list), len(x)))
    masd = np.zeros((1, len(x)))
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
        y += mins
        mas[file] = y
    for i in range(len(mas)):
        delta = np.mean(mas[i][maxs - 50 : maxs + 50])
        d = delta_m - delta
        if d <= 0.025:
            masd = np.append(masd, [mas[i]], axis=0)
    if len(masd) == 1:
        continue
    nfiles = round(len(masd) * 100 / len(mas), 2)
    masd = sm(masd)
    maxd = np.max(masd)
    cor = cord(masd)
    a = np.arange(cor[0], cor[1])

    index_max = x[np.argmax(masd)]
    index_max_min = maxd / np.mean(masd[c1:c2])
    weight = cor[1] - cor[0]
    color = color_list[folder]
    label = (
        "синтез №"
        + current_folder
        + " "
        #  + str(nfiles)
        + "\n"
        + str(round(index_max, 2))
        + "нм "
        + str(round(index_max_min, 2))
        + " "
        # + str(round(weight, 2))
        #  + "нм"
    )

    data[p][0] = current_folder
    data[p][1] = index_max
    data[p][2] = index_max_min
    data[p][3] = weight
    p += 1

    ax.plot(
        x,
        masd,
        linewidth=1.5,
        label=label,
        color=color,
    )
    # ax.plot(a, np.ones(len(a)) * maxd * 0.75, linestyle="dashed", color=color)
    ax.legend()
    # bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.legend(
        #  bbox_to_anchor=(1.01, 1),
        loc="upper right",
        borderaxespad=0.0,
    )
    plt.xlabel("Длина волны, нм")
    plt.ylabel("Интенсивность, отн.ед")


print("Elapsed time: ", time.time() - start_time)


wb = Workbook()
ws = wb.active

for r_num, row in enumerate(data, start=1):
    for c_num, value in enumerate(row, start=1):
        ws.cell(row=r_num, column=c_num).value = value

wb.save("output.xlsx")


plt.ioff()
plt.show()
