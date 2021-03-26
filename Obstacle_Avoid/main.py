# Obstacle Avoidance

from rplidar import RPLidar
import math
from numpy import genfromtxt
import numpy as np

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50

x_dest = float(1.39626)
y_dest = float(560)  # obtained from path planning
xref = float(1.42)  # gps location?
yref = float(400)


def obs_avoid():
    lidar_data = genfromtxt('lidar_data.csv', delimiter=',')
    lidar_data = np.asarray(lidar_data)
    x_obs = lidar_data[:, 0]
    y_obs = lidar_data[:, 1]
    # print(a)
    # print(d)

    count = 0
    max = 0  # max distance between points
    jc = 0  # renamed j iterator to jc
    flag = 0
    dist_dest = math.sqrt(math.pow((x_dest - xref), 2) + math.pow((y_dest - yref),
                                                                  2))  # distance between initial point and destination
    print("distdest", dist_dest)

    print("xobs", x_obs)
    print("yobs", y_obs)
    # for j in range(0, len(x_obs) - 1):
    #     dist = math.sqrt(math.pow((x_obs[j] - x_obs[j + 1]), 2) + math.pow((y_obs[j] - y_obs[j + 1]),
    #                                                                        2))  # distance between 2 points
    #     print("Distance between 2 points:", dist)
    #     if max < dist:
    #         max = dist
    #         jc = j
    # print("Max distance between points: ", max)
    # print("jc", jc)
    # # slope
    # m = (y_obs[jc + 1] - y_obs[jc]) / (x_obs[jc + 1] - x_obs[jc])  # slope of line
    # print("Slope", m)

    # 2. Optimal Travelling Angle
    theta = math.radians(math.atan((y_dest - yref) / (x_dest - xref)))  # optimal travelling angle
    print("Optimal Travelling Angle in radians: ", theta)

    # # dist1
    # dist1 = abs((m * x_obs[jc]) - y_obs[jc]) / (math.sqrt(1 + math.pow(m, 2)))
    # print("dist1: ", dist1)
    orient_angle = 0  # set orientation angle
    # gamma = math.degrees(math.acos(dist1 / (math.sqrt(math.pow(x_obs[jc], 2) + math.pow(y_obs[jc], 2)))))
    # print("Gamma: ", gamma)

    alpha = theta  # current travelling direction, this will need to get updated

    print("alpha", alpha)

    diff = alpha - theta
    max_dist = 200

    for j in range(0, len(y_obs)):
        # obstacle not detected
        if (y_obs[j] - yref) > max_dist: # this needs to change
            for i in range(j, j + 1):
                if y_obs[j] > dist_dest:
                    if diff == 0:
                        orient_angle = theta
                    elif diff > 0:
                        orient_angle = alpha + diff
                    elif diff < 0:
                        orient_angle = alpha - diff
                    flag = 1
                else:
                    flag = 0
        print("orient angle 1", orient_angle)

        # obstacle detected
        if (y_obs[j] - yref) < max_dist:
            # set temp path
            alpha_temp = 90
            alpha_temp = np.radians(alpha_temp)
            orient_angle2 = orient_angle + alpha_temp

            diff_2 = alpha_temp - theta
            if y_obs[j] > dist_dest:
                if diff > 0:
                    orient_angle2 = alpha_temp + diff_2
                elif diff < 0:
                    orient_angle2 = alpha_temp - diff_2
                flag = 1
            else:
                flag = 0
            print("orient angle 2", orient_angle2)

    if flag == 1:  # this will be sent to the bot
        # not sure how to do this
        orient_angle = round(orient_angle, 2)


if __name__ == '__main__':
    obs_avoid()
