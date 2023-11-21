for i in range(len(li)):
    a = len(li[i]) - 1
    if a > 0:
        li[i] = np.sum(li[i], axis=0)
        li[i] = np.divide(li[i], a)
        li[i] = signal.savgol_filter(li[i], 60, 3)
        lmax = np.argmax(li[i]) * step_v + start
        imin = np.mean(li[i][c1:c2])
        imax = np.max(li[i])
        label = (
            str(round((i) * step, 4))
            + "-"
            + str(round((i + 1) * step, 4))
            + "\n"
            + str(round(a / len(file_list) * 100, 2))
            + "% "
            + str(round(lmax, 2))
            + "нм "
            + str(round(imax / imin, 2))
        )

        plt.plot(x, li[i], label=label)
        # plt.plot(x, li[i], label=current_folder_path)


with open("data.txt", "w") as file:
    for line in range(len(data)):
        print(data[line])
        for i in range(4):
            file.write(str(data[line][i]) + "\t")
        file.write("\n")
    file.close()
