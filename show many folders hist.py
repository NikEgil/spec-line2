import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
from scipy import signal
import time
import re
from pylab import *
import seaborn as sns

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
print(start_point, start_max_point)


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
cmap = cm.get_cmap("jet", len(folders_list))
color_list = [matplotlib.colors.rgb2hex(cmap(i)[:3]) for i in range(cmap.N)]

start_time = time.time()

steps = 0.01
# len(folders_list)
bins1 = np.arange(0, 0.3, steps)
bins2 = np.arange(0, 0.2 - steps, steps) + steps / 2
c1 = round((400 - start) / step)
for folder in range(len(folders_list)):
    current_folder_path = main_folder + "/" + folders_list[folder] + "/"
    current_folder = folders_list[folder]
    file_list = np.array(os.listdir(current_folder_path))

    print("in " + current_folder + " graphs ", len(file_list))
    mas = np.zeros(0)
    for file in range(len(file_list)):
        spec = open(current_folder_path + file_list[file], "r", encoding="utf8")
        y = get_rmr(spec.read())

        # дельта с предпологаемой областью
        # a = np.mean(y[start_max_point : start_max_point + 100]) - np.mean(
        #     y[start_mean_point:end_mean_point]
        #  )
        # дельта с максимумом
        # a = np.max(y) - np.mean(y[start_mean_point:end_mean_point])
        mas = np.append(mas, np.max(y))
    sns.histplot(data=mas, bins=bins1, kde=True)
# hist, bins = np.histogram(mas, bins1)
# maxs = np.max(hist)
# mins = np.min(hist)
# scaled_data = (hist - mins) / (maxs - mins)

#  plt.plot(
#      bins2, scaled_data, color=color_list[len(ax.get_lines())], label=current_folder
#  )
#  plt.legend()

print("Elapsed time: ", time.time() - start_time)

plt.ioff()
plt.show()
