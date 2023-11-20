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
start_mean_point = int(len_y * 0.8)
end_mean_point = int(len_y * 0.9)
y = np.zeros(len_y)
x = np.arange(start + step, end, step)
# endregion
start_max_point = round(len_y * 0.27)
print(start_max_point, len_y)


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


plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)


start_time = time.time()

# len(folders_list)
steps = 0.0125
bins1 = np.arange(0, 0.2, steps)
bins2 = np.arange(steps / 2, 0.2 - steps / 2, steps)

num_folders = 2
# num_folders=len(folders_list)
for folder in range(12, 13):
    current_folder_path = main_folder + "/" + folders_list[folder] + "/"
    current_folder = folders_list[folder]
    file_list = np.array(os.listdir(current_folder_path))

    print("in " + current_folder + " graphs ", len(file_list))
    mas = np.zeros(0)

    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        a = np.mean(y[start_max_point : start_max_point + 50]) - np.mean(
            y[start_mean_point:end_mean_point]
        )

        mas = np.append(mas, a)
        hist, bins = np.histogram(mas, bins1)
        min_val = np.min(hist)
        max_val = np.max(hist)

        scaled = (hist - min_val) / (max_val - min_val)
    plt.plot(bins2, scaled, label="область 0,27-0,3")
    plt.legend()

    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        maxs = np.argmax(y)
        a = np.mean(y[maxs - 50 : maxs + 50]) - np.mean(
            y[start_mean_point:end_mean_point]
        )

        mas = np.append(mas, a)
        hist, bins = np.histogram(mas, bins1)
        min_val = np.min(hist)
        max_val = np.max(hist)

        scaled = (hist - min_val) / (max_val - min_val)
    plt.plot(bins2, scaled, label="область max")
    plt.legend()

    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        maxs = np.argmax(y[0 : round(len_y / 2)])
        a = np.mean(y[maxs - 50 : maxs + 50]) - np.mean(
            y[start_mean_point:end_mean_point]
        )

        mas = np.append(mas, a)
        hist, bins = np.histogram(mas, bins1)
        min_val = np.min(hist)
        max_val = np.max(hist)

        scaled = (hist - min_val) / (max_val - min_val)
    plt.plot(bins2, scaled, label="область max в первой половине")
    plt.legend()
    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())
        a = np.max(y) - np.mean(y[start_mean_point:end_mean_point])

        mas = np.append(mas, a)
        hist, bins = np.histogram(mas, bins1)
        min_val = np.min(hist)
        max_val = np.max(hist)

        scaled = (hist - min_val) / (max_val - min_val)
    plt.plot(bins2, scaled, label="просто max")
    plt.legend()

print("Elapsed time: ", time.time() - start_time)

plt.ioff()
plt.show()
