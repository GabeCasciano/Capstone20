# Obstacle Avoidance

from rplidar import RPLidar
import math
from numpy import genfromtxt
import numpy as np

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50

x_dest = []
y_dest = []  # obtained from path planning
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
    max = 0
    jc = 0
    for j in range(0, len(d)):
        x_current.append((d[count]) * (math.cos(a[count])))
        y_current.append((d[count]) * (math.sin(a[count])))
        count = count + 1
    for j in range(0, len(x_current) - 1):
        dist = math.sqrt(
            math.pow((x_current[j] - x_current[j + 1]), 2) + math.pow((y_current[j] - y_current[j + 1]), 2))
        # print(dist)
        if max < dist:
            max = dist
            jc = j
    print(max)
    print(jc)
    # slope
    m = (y_current[jc + 1] - y_current[jc]) / (x_current[jc + 1] - x_current[jc])
    print(m)

    # 2. Optimal Travelling Angle
    theta = math.degrees(math.atan((y_dest - yref) / (x_dest - xref)))
    print("Optimal Travelling Angle: ", theta)

    # dist1
    dist1 = abs((m*x_current[jc]) - y_current[jc]) / (x_current[jc+1]-x_current)
    orient_angle = 0  # set orientation angle
    alpha = y_current  # current travelling direction

     if obs_det:
         # 4. obstacle detected

         dist_obs1 = (x_dest, y_dest) - (x_current, y_current)
         dist_obs2 = obs_det - (x_current, y_current)

         if dist_obs2 >= dist_obs1:
             orient_angle = theta
         else:
             # turn orient_angle 90 deg (temporary path)
             alpha_temp = (x_current, y_current)
             diff = alpha_temp - theta
             new_dir = diff

             if new_dir > 0:
                 orient_angle = alpha_temp + new_dir
             else:
                 orient_angle = alpha_temp - new_dir
     else:
         # 3. obstacle not detected

         diff = alpha - theta  # diff

         if diff == 0:
             orient_angle = theta
         elif diff > 0:
             orient_angle = alpha + diff
         elif diff < 0:
             orient_angle = alpha - diff


# def run():
#
#         # 1. current location
#      if x_current == x_dest and y_current == y_dest:
#          # stop system
#      else:
#          obs_avoid()


if __name__ == '__main__':
    obs_avoid()
