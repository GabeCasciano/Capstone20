# Obstacle Avoidance

from rplidar import RPLidar
import math
from numpy import genfromtxt
import numpy as np

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50

x_dest = float(2.67)
y_dest = float(560)  # obtained from path planning
xref = 0
yref = 0


def obs_avoid():
    lidar_data = genfromtxt('lidar_data.csv', delimiter=',')
    lidar_data = np.asarray(lidar_data)
    a = lidar_data[:, 0]
    d = lidar_data[:, 1]
    # print(a)
    # print(d)
    x_current = []
    y_current = []
    count = 0
    max = 0 # max distance between points
    jc = 0 # renamed j iterator to jc
    flag = 0
    dist_dest = math.sqrt(math.pow((x_dest - xref), 2) + math.pow((y_dest - yref),
                                                                  2))  # distance between initial point and destination
    print("distdest",dist_dest)
    for j in range(0, len(d)):
        x_current.append((d[count]) * (math.cos(a[count])))
        y_current.append((d[count]) * (math.sin(a[count])))
        count = count + 1
    for j in range(0, len(x_current) - 1):
        dist = math.sqrt(math.pow((x_current[j] - x_current[j + 1]), 2) + math.pow((y_current[j] - y_current[j + 1]), 2)) # distance between 2 points
        print("Distance between 2 points:", dist)
        if dist > max:
            max = dist
            jc = j
    print("Max distance between points: ", max)
    print("jc", jc)
    # slope
    m = (y_current[jc + 1] - y_current[jc]) / (x_current[jc + 1] - x_current[jc]) # slope of line
    print("Slope", m)

    # 2. Optimal Travelling Angle
    theta = math.radians(math.atan((y_dest - yref) / (x_dest - xref))) # optimal travelling angle
    print("Optimal Travelling Angle in radians: ", theta)

    # dist1
    dist1 = abs((m * x_current[jc]) - y_current[jc]) / (math.sqrt(1 + math.pow(m, 2)))
    print("dist1: ", dist1)
    orient_angle = 0  # set orientation angle
    gamma = math.degrees(math.acos(dist1 / (math.sqrt(math.pow(x_current[jc], 2) + math.pow(y_current[jc], 2)))))
    print("Gamma: ", gamma)

    alpha = theta  # current travelling direction, this will need to get updated

    print("alpha", alpha)

    diff = alpha - theta

    for j in range(0, len(d)):
        # obstacle not detected
        if theta - gamma < a[j] < theta + gamma:
            for i in range(j, j+1):
                if d[j] > dist_dest:
                    if diff == 0:
                        orient_angle = theta
                    elif diff > 0:
                        orient_angle = alpha + diff
                    elif diff < 0:
                        orient_angle = alpha - diff
                    flag = 1
                else:
                    flag = 0
        print(orient_angle)

        # dist_obs1 = (x_dest, y_dest) - (x_current, y_current)
        # dist_obs2 = obs_det - (x_current, y_current)
    #
    #     if dist_obs2 >= dist_obs1:
    #         orient_angle = theta
    #     else:
    #         # turn orient_angle 90 deg (temporary path)
    #         alpha_temp = (x_current, y_current)
    #         diff = alpha_temp - theta
    #         new_dir = diff
    #
    #         if new_dir > 0:
    #             orient_angle = alpha_temp + new_dir
    #         else:
    #             orient_angle = alpha_temp - new_dir
    # else:
    #     # 3. obstacle not detected
    #
    #     diff = alpha - theta  # diff

    if flag == 1: # this will be sent to the bot
        # not sure how to do this
        orient_angle = round(orient_angle, 2)



if __name__ == '__main__':
    obs_avoid()
