from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50
lidar = RPLidar(PORT_NAME)
iterator = lidar.iter_scans()


def update_line():
    scan = next(iterator)
    offsets = np.array([(np.radians(point[1]), point[2]) for point in scan])
    x = range_filter(offsets, 0, 1000)
    x = np.asarray(x)  # saves array as rows
    x = np.transpose(x)  # transpose to col
    offsets[:, 1] = x
    offsets = offsets[np.all(offsets != 0, axis=1)]  # removes rows with 0s
    thres = distance_threshold(offsets, 20)  # distance threshold function
    thres_col2 = thres[:, 2].reshape(-1, 1)
    # add segment value column to offset array to plot
    offsets = np.append(offsets, thres_col2, axis=1)
    # with open("test.csv", "wb") as f:
    # f.write(b'Angle, Distance, Seg Num \n')
    np.savetxt('lidar_data.csv', offsets, delimiter=',', fmt='%1.5f')
    # ident = struct_ident(offsets)
    # line.set_offsets(offsets)



    # separate segments and plot
    x = offsets[:, 0]
    y = offsets[:, 1]
    last = len(offsets[:, 2])
    last = int(offsets[last - 1, 2])
    check = 1
    count = 0
    abc = 0

    for i in range(1, last):
        for j in range(len(offsets[:, 2])):

            if check == offsets[j, 2]:
                count += 1
            if check != offsets[j, 2] or j == len(offsets[:, 2]) - 1:
                check = offsets[j, 2]
                a = x[abc:count]
                b = y[abc:count]
                a = np.asarray(a)
                b = np.asarray(b)
                count += 1
                abc = count - 1
                # plt.polar(a, b)
                # plt.show()

    # intens = np.array([point[0] for point in scan])
    # line.set_array(intens)
    # plot = line_seg(offsets)  # fix this
    return offsets,


def range_filter(scans, dmin, dmax):
    # assuming we have to define max and min from distance values- so 0 to 1000
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
    # conditions where segment threshold > 20 mm, can be changed
    cond_1 = thres[:, 1] > seg_threshold
    check = np.where(cond_1, 2, 1)  # check where its true or false
    check = check.reshape(-1, 1)
    iter_seg = 1
    for k in range(len(check)):
        if check[k] == 2:  # true
            iter_seg = iter_seg + 1  # iterate to next segment
            check[k] = iter_seg
        elif check[k] == 1:  # false: diff between 2 distances is less than threshold
            check[k] = iter_seg  # same segment
    thres[:, 2] = check[:, 0]
    return thres


if __name__ == '__main__':
    dmin = 0
    dmax = 1500
    update_line()
    lidar.stop()
    lidar.disconnect()

# def run():
#     lidar = RPLidar(PORT_NAME)
#     dmin = 0
#     dmax = 1500
#
#     fig = plt.figure()
#     ax = plt.subplot(111, projection='polar')
#
#     line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
#                       cmap=plt.cm.Greys_r, lw=0)
#     ax.set_rmax(dmin)
#     ax.set_rmax(dmax)
#     ax.grid(True)
#     iterator = lidar.iter_scans()
#     # update_line(iterator, offsets, line)
#     # include jupyter stuff
#     ani = animation.FuncAnimation(fig, update_line, fargs=(iterator, line), interval=50)
#     plt.show()
#     lidar.stop()
#     lidar.disconnect()
