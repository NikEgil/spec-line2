import sys

import matplotlib.pyplot as plt
import numpy as np


def on_press(event):
    print("press", event.key)
    sys.stdout.flush()
    if event.key == "x":
        visible = xl.get_visible()
        xl.set_visible(not visible)
        fig.canvas.draw()


# Fixing random state for reproducibility
np.random.seed(19680801)

fig, ax = plt.subplots()

fig.canvas.mpl_connect("key_press_event", on_press)

ax.plot(np.random.rand(12), np.random.rand(12), "go")
xl = ax.set_xlabel("easy come, easy go")
ax.set_title("Press a key")
plt.show()


def car(path_folder, file_list, s):
    for i in range(s, s + size):
        print(s)
        spec = open(str(path_folder + file_list[i]), "r", encoding="utf8")
        spec = spec.read().split(",")
        for j in range(start_point, end_point):
            y[j - start_point] = float(spec[j + 11])
        # z = exponential_smoothing(y,alpha)
        z = signal.savgol_filter(y, 51, 3)
        # plt.plot(x,y, label=file_list[s])
        # plt.plot(x,z, label=file_list[s]+" sm")
        plt.plot(x, y, label="original", color="royalblue", linewidth=1)
        plt.plot(x, z, label="smooth", color="darkorange", linewidth=1)
        mean = np.mean(z[len(z) - 150 : len(z)])
        plt.plot(x, z - mean, label="down", color="green", linewidth=1)

        print(mean)

    plt.legend(loc=1)
    plt.show()


def exponential_smoothing(series, alpha):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


plt.show()


while stat == True:
    a = input()
    if a == "1":
        plt.clf()
        plt.cla()
        s += size
        car(path_folder, file_list, s)

    if a == "2":
        plt.clf()
        plt.cla()
        s -= size
        car(path_folder, file_list, s)
    if a == "3":
        plt.close()
        break




Elapsed time:  3.169907808303833
3.1751585006713867