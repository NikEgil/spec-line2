import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal

mas = np.ones((1, 5))
print(mas)
a = np.array([1, 2, 3, 4, 5])

mas = np.append(mas, [a], axis=0)
print(mas)
print(np.sum(mas, axis=0))


print(chr(92))


main_folder = r"C:\Users\Nik\Desktop\prog\data3"
main_folder = main_folder.replace(chr(92), "/") + "/"
print(main_folder)
folders_list = np.array(os.listdir(main_folder))
print(folders_list)

# region переменные
crit = 0.1
# 153 884    измеряемый диапазон. 0-2136 диапазон данных
start = 400  # нм
end = 700  # нм
step = (884 - 153) / 2134

start_point = round((start - 153) / step)
end_point = start_point + int((end - start) / step)

print(step, start_point, end_point)
y = np.zeros(int((end - start) / step))

x = np.arange(start + step, end, step)
# endregion


for a in range(len(folders_list)):
    current_folder = main_folder + "/" + folders_list[a] + "/"
    print(current_folder)
    file_list = np.array(os.listdir(current_folder))
    print(file_list[a][-1])
    print(current_folder + file_list[a])
    spec = open(current_folder + file_list[file], "r", encoding="utf8")
    spec = spec.read().split(",")
    print(spec)
    for file in range(len(file_list)):
        for j in range(start_point, end_point):
            y[j - start_point] = float(spec[j + 11])


if len(mas) > 1:
    a = len(mas) - 1

    mas = np.sum(mas, axis=0)
    mas = np.divide(mas, a)
    mas = signal.savgol_filter(mas, 60, 3)
    ax.plot(
        x,
        mas,
        linewidth=1.5,
        label=current_folder,
        alpha=1,
        color=color_list[len(ax.get_lines())],
    )
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", borderaxespad=0.0)
    fig.canvas.draw()
    fig.canvas.flush_events()
    print("used graphs " + str(a))
else:
    print("no graphs")
    pass
