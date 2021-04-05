# Obstacle Avoidance

from numpy import genfromtxt
import numpy as np
import math

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50




def obs_avoid():
    x_dest = [1.39626]
    y_dest = [560]  # obtained from path planning
    xref = [1.42]  # gps location- will be saved as np arrays
    yref = [400]

    xref = np.asarray(xref)
    yref = np.asarray(yref)
    x_dest = np.asarray(x_dest)
    y_dest = np.asarray(y_dest)

    lidar_data = [[1.09356, 550.25, 2],
                  [1.11537, 530, 2],
                  [1.1391, 539.75, 2],
                  [1.16337, 550.25, 2],
                  [1.18437, 562, 2],
                  [1.207, 576.5, 2],
                  [1.228, 595.5, 3],
                  [1.25527, 569, 3],
                  [1.27491, 572.5, 3],
                  [1.29918, 574.75, 3],
                  [1.32481, 578.25, 3],
                  [1.34472, 578.5, 3],
                  [1.36708, 588.25, 3],
                  [1.39272, 607.75, 3],
                  [1.41181, 617.25, 3],
                  [1.43499, 627.25, 3],
                  [1.45899, 636.25, 3],
                  [1.48135, 649, 3],
                  [1.50235, 666, 4],
                  [1.79987, 261.25, 5],
                  [1.93895, 796.75, 6],
                  [1.97304, 603.5, 6],
                  [1.99649, 589.5, 6],
                  [2.0224, 586.25, 6],
                  [2.04285, 593.25, 7],
                  [2.17866, 230.25, 7],
                  [2.17975, 231.25, 7],
                  [2.22966, 232.5, 7],
                  [2.25284, 237.25, 7],
                  [2.27247, 233.25, 7],
                  [2.30165, 235.5, 7],
                  [2.33029, 235.75, 7],
                  [2.3881, 244.25, 7],
                  [2.41346, 245, 7],
                  [2.43719, 247, 7],
                  [2.46255, 249.5, 7],
                  [2.47264, 252.5, 7],
                  [2.50373, 255.25, 7],
                  [2.52336, 258.5, 7],
                  [2.54491, 262, 7],
                  [2.57191, 265.5, 7],
                  [2.59536, 269.5, 7],
                  [2.61772, 273.5, 7],
                  [2.62536, 277.75, 7],
                  [2.65699, 282.25, 7],
                  [2.67554, 287, 7],
                  [2.69435, 292.25, 7],
                  [2.72817, 299.25, 7],
                  [2.76035, 309.75, 7],
                  [2.78625, 316.5, 7]]
    # lidar_data = genfromtxt('lidar_data.csv',
    # delimiter=',')  # should we change from the csv to direct np arrays from obst detection func
    lidar_data = np.asarray(lidar_data)
    obs_flag = 0

    x_obs = lidar_data[:, 0]
    y_obs = lidar_data[:, 1]

    diff_x = abs(x_obs - xref)
    diff_y = abs(y_obs - yref)

    diff_x = np.all(diff_x)
    diff_y = np.all(diff_y)

    dist_dest = math.sqrt(math.pow((x_dest - xref), 2) + math.pow((y_dest - yref),
                                                                  2))  # distance between initial point and destination

    # Optimal Travelling Angle
    theta = abs(math.radians(math.atan((y_dest - yref) / (x_dest - xref))))  # optimal travelling angle
    print("Optimal Travelling Angle in radians: ", theta)

    orient_angle = [0]  # set orientation angle

    diff_angle = xref - theta
    max_dist = 200

    for j in range(0, len(y_obs)):

        if (diff_x > 20) and (diff_y > 20):  # obst not detected close by
            for i in range(j, j + 1):
                if y_obs[j] > dist_dest:
                    if diff_angle == 0:
                        orient_angle = theta
                    elif diff_angle > 0:
                        orient_angle = xref + diff_angle
                    elif diff_angle < 0:
                        orient_angle = xref - diff_angle
                    obs_flag = 1
                else:
                    obs_flag = 0
                print("orient angle 1", orient_angle)

        elif (diff_x < 20) and (diff_y < 20):  # obs detected close by
            # set temp path
            alpha_temp = 90
            alpha_temp = np.radians(alpha_temp)
            orient_angle2 = theta + alpha_temp

            diff_2 = alpha_temp - theta
            if y_obs[j] > dist_dest:
                if diff_2 > 0:
                    orient_angle2 = alpha_temp + diff_2
                elif diff_2 < 0:
                    orient_angle2 = alpha_temp - diff_2
                obs_flag = 1
            else:
                obs_flag = 0
            print("orient angle 2", orient_angle2)

    if obs_flag == 0:
        # condition basically telling bot to go normally, idk
        xref = 0  # alpha= current travelling angle, NEED TO GET FROM IMU
        print("0")
    elif obs_flag == 1:
        # set it to follow orientation angle
        orient_angle
        print("1")


if __name__ == '__main__':
    obs_avoid()
