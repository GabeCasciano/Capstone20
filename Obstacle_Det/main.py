from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50


def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(point[1]), point[2]) for point in scan])
    x = range_filter(offsets, 0, 1000)
    x = np.asarray(x)  # saves array as rows
    x = np.transpose(x)  # transpose to col
    offsets[:, 1] = x
    offsets = offsets[np.all(offsets != 0, axis=1)]  # removes rows with 0s
    thres = distance_threshold(offsets, 20) # distance threshold function
    line.set_offsets(thres)
    intens = np.array([point[0] for point in scan])
    line.set_array(intens)
    return line,


def range_filter(scans, dmin, dmax):
    # assuming we have to define max and min from distance values- so 0 to 2500?
    x = scans[:, 1]
    for i in range(len(x)):
        if x[i] < dmin:
            x[i] = 0
        elif x[i] > dmax:
            x[i] = 0
    return x


def distance_threshold(scans, seg_threshold):
    i = 1  # incremental num
    temp = scans[:, 1]
    thres = np.zeros((len(temp), 3))
    thres[:, 0] = temp
    x = [temp[len(temp) - 1]]
    np.asarray(x)
    temp = np.append(temp, x, axis=0)
    thres[:, 1] = abs(np.diff(temp, axis=0))
    cond_1 = thres[:, 1] > seg_threshold    # conditions where segment threshold > 20 mm, can be changed
    check = np.where(cond_1, 2, 1)
    check = check.reshape(-1, 1)
    iter_seg = 1
    for k in range(len(check)):
        if check[k] == 2:
            iter_seg = iter_seg + 1
            check[k] = iter_seg
        elif check[k] == 1:
            check[k] = iter_seg
    thres[:, 2] = check[:, 0]
    return thres


def run():
    lidar = RPLidar(PORT_NAME)
    dmin = 0
    dmax = 1500

    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                      cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(dmin)
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


