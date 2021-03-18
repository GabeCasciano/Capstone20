# Obstacle Avoidance

from rplidar import RPLidar
import math

PORT_NAME = '/COM3'
IMIN = 0
IMAX = 50

x_current = 0
y_current = 0
x_dest = []
y_dest = [] # obtained from path planning

def obs_det():
    # create a flag
    # read numpy array of data https://stackoverflow.com/questions/3518778/how-do-i-read-csv-data-into-a-record-array-in-numpy



def obs_avoid():

    # 2. Optimal Travelling Angle
    theta = math.degrees(math.atan((y_dest-y_current)/(x_dest-x_current)))
    print("Optimal Travelling Angle: ", theta)
    orient_angle = 0  # set orientation angle
    alpha = y_current # current travelling direction

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


        diff = alpha - theta    # diff

        if diff == 0:
            orient_angle = theta
        elif diff > 0:
            orient_angle = alpha + diff
        elif diff < 0:
            orient_angle = alpha - diff

def run():
    # 1. current location
    if x_current == x_dest and y_current == y_dest:
        # stop system
    else:
        obs_avoid()


if __name__ == '__main__':
    run()


