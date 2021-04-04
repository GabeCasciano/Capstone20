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
    obs_det = np.array([(np.radians(point[1]), point[2]) for point in scan])
    x = range_filter(obs_det, 0, 1000)
    x = np.asarray(x)  # saves array as rows
    x = np.transpose(x)  # transpose to col
    obs_det[:, 1] = x
    obs_det = obs_det[np.all(obs_det != 0, axis=1)]  # removes rows with 0s
    thres = segmentation(obs_det, 20)  # distance threshold function
    thres_col2 = thres[:, 2].reshape(-1, 1)
    # add segment value column to offset array to plot
    obs_det = np.append(obs_det, thres_col2, axis=1)
    np.savetxt('lidar_data.csv', obs_det, delimiter=',', fmt='%1.5f')

    return obs_det,


def range_filter(scans, dmin, dmax):
    # assuming we have to define max and min from distance values- so 0 to 1000
    x = scans[:, 1]
    for i in range(len(x)):
        if x[i] < dmin:
            x[i] = 0
        elif x[i] > dmax:
            x[i] = 0
    return x


def segmentation(scans, seg_threshold):
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

