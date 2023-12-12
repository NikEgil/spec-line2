import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import statistics as st
from scipy import stats
from scipy import signal
import re
from sklearn.neighbors import KernelDensity

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
method = 0
s = 0  # начальная папка

# fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12, 4)) layout="constrained", sharey=True

fig, ax = plt.subplots(1, 1)


def get_rmr(spec):
    spec = re.split(",", spec)
    for j in range(start_point, end_point):
        y[j - start_point] = float(spec[j + 11])
    return y


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


def hist(mas, ind):
    ar = np.zeros(len(mas))
    if ind == "max":
        for i in range(len(mas)):
            ar[i] = np.max(mas[i])
    else:
        for i in range(len(mas)):
            ar[i] = mas[i][ind]
    return ar


def density(x):
    dx = x.max() - x.min()
    if dx == 0:
        return [x[0] - 1, x[0] - 0.01, x[0], x[0] + 0.01, x[0] + 1], [0, 0, 1, 0, 0]
    kde_sk = KernelDensity(bandwidth=dx / 50, kernel="gaussian")
    kde_sk.fit(x.reshape([-1, 1]))
    eval_points = np.linspace(x.min() - dx * 0.1, x.max() + dx * 0.1, 100)
    y_sk = np.exp(kde_sk.score_samples(eval_points.reshape(-1, 1)))
    return eval_points, y_sk


def car(current_folder_path, s):
    plt.cla()
    plt.clf()
    plt.show()
    global n

    file_list = np.array(os.listdir(current_folder_path))
    mas = np.zeros((len(file_list), len_y))
    for file in range(len(file_list)):
        with open(current_folder_path + file_list[file], "r", encoding="utf8") as spec:
            y = get_rmr(spec.read())
        # mas[file] = signal.savgol_filter(y, 60, 3)
        # t = signal.savgol_filter(y, 60, 3)
        # y[[lamp_point, mean_point]] = t[[lamp_point, mean_point]]
        mas[file] = signal.savgol_filter(y, 60, 3)

    plt.suptitle(
        "скопления, синтез " + current_folder_path[-3:] + str(len(file_list)) + "шт"
    )
    histplot(mas, 1, "I")

    m = np.zeros((len(file_list), len_y))

    for i in range(len(mas)):
        m[i] = mas[i] - mas[i][mean_point]
    histplot(m, 6, "вычитание I(650нм)")

    for i in range(len(mas)):
        m[i] = mas[i] - mas[i][lamp_point]
    histplot(m, 11, "вычитание I(565нм)")

    for i in range(len(mas)):
        m[i] = mas[i] - mas[i][mean_point]
        m[i] = m[i] / m[i][lamp_point]
    histplot(m, 16, "- I(650нм) / I(565нм)")

    plt.show()


def histplot(mas, n, tex):
    # гист в 420
    plt.subplot(4, 5, n)
    if n == 1:
        plt.title(label="420нм")
    plt.ylabel(tex)
    h = hist(mas, min_point)
    bins1 = np.arange(np.min(h), np.max(h), np.max(h) / 100)
    bins2 = np.arange(np.min(h), np.max(h) - np.max(h) / 100, np.max(h) / 100)
    # counts, bins = np.histogram(h, bins1)

    plt.plot(*density(h))

    # гист в max
    plt.subplot(4, 5, n + 1)
    if n == 1:
        plt.title(label="max")
    h = hist(mas, "max")
    # counts, bins = np.histogram(h, bins1)
    plt.plot(*density(h))

    # гист в 565 лампа
    plt.subplot(4, 5, n + 2)
    if n == 1:
        plt.title(label="565нм")
    h = hist(mas, lamp_point)
    # counts, bins = np.histogram(h, bins1)
    plt.plot(*density(h))

    # гист в 650
    plt.subplot(4, 5, n + 3)
    if n == 1:
        plt.title(label="650нм")
    h = hist(mas, mean_point)
    # counts, bins = np.histogram(h, bins1)
    plt.plot(*density(h))

    plt.subplot(4, 5, n + 4)
    if n == 1:
        plt.title(label="все графики")
    for i in range(len(mas)):
        # a = signal.savgol_filter(mas[i], 60, 3)
        plt.plot(x, mas[i], color="black", lw=0.2, alpha=0.1)


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    global s
    global size
    global method
    current_folder_path = main_folder + "/" + str(folders_list[s]) + "/"
    if event.key == "1":
        plt.cla()
        plt.clf()
        plt.show()
    if event.key == "2":
        plt.savefig(str(current_folder_path[-3:]))
    if event.key == "right":
        s = s + 1
        car(current_folder_path, s)
    if event.key == "left":
        s = s - 1
        car(current_folder_path, s)
    print(s, current_folder_path)
    plt.savefig(str(current_folder_path[-3:-1]))


file_list = []
fig.canvas.mpl_connect("key_press_event", on_press)
plt.show()
