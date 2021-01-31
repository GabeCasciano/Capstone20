from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import statistics

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50


def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(point[1]), point[2]) for point in scan])
    # print(offsets.shape)
    x = range_filter(offsets, 0, 1000)
    x = np.asarray(x)
    x = np.transpose(x)
    # print(x.shape)
    offsets[:, 1] = x
    # offsets = temp_median_filter(offsets, 2000)
    line.set_offsets(offsets)
    intens = np.array([point[0] for point in scan])
    line.set_array(intens)
    return line,


def range_filter(scans, dmin, dmax):
    # assuming we have to define max and min from distance values- so 0 to 2500?
    # line =
    # for point in scans:
    x = scans[:, 1]
    for i in range(len(x)):
        if x[i] < dmin:
            x[i] = 0
        elif x[i] > dmax:
            x[i] = 0
    return x


# return [[min(max(point[1], dmin), dmax) for point in scans]]  # found this way, tryna implemenet something else tho


#
#
# def temp_median_filter(scans, d):
#     result = []
#     for current in range(len(scans)):
#         medians = []
#         try:
#             for previousIndex in range(len(scans[current])):
#                 # change this from statistics to angle and distance?
#                 medians.append(statistics.median([scan[previousIndex]
#                                                   for scan in scans[max(-1, current - d) + 1: current + 1]]))
#         except IndexError as err:
#             print(err)
#         #             #exit()  # comment this line if u still want the values with varied scans
#         result.append(medians)
#     return result


def run():
    lidar = RPLidar(PORT_NAME)
    dmin = 0
    dmax = 2500

    # d = 3
    #
    # # calling functions and error handling for varied scan lengths
    # filter1_value = range_filter(update_line, dmin, dmax)
    # filter2_value = list(temp_median_filter(filter1_value, d + 1))
    #
    # print("input", update_line, "\n""after_MixMax_filter", filter1_value, "\n""After_temp_median:", filter2_value)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                      cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(dmax)
    ax.grid(True)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
                                  fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    run()
