from Autonomous.Sensors.LIDAR import LIDAR_Interface, Utils
from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion
from Autonomous.Modules.Obstacle_Detection import Obstacle_Detection
from Autonomous.Modules.Path_Planning import Path
import numpy as np
import math

class Obstacle_Avoidance:

    SF = Sensor_Fusion()
    Obs_Det = Obstacle_Detection()
    PP = Path()

    def __init__(self):

        self.__running = False
        self.x_ref = self.SF.gps_latitude
        self.y_ref = self.SF.gps_longitude
        self.__obstacle = self.Obs_Det.detected_obstacle
        self.x_dest = self.PP._dest_lat
        self.y_dest = self.PP.destination_long

        self.__obstacle_flag = False
        self.__orient_angle = np.asarray[0]
        # self.__orient_angle_det = np.asarray[0]


    def avoid_obstacle(self, __obstacle:tuple, __obstacle_flag, __orient_angle):
        # obstacle is the location of the obstacle relative to the robot
        # direction represents going to the left around the obstacle if false
        # uses the self.__running var to indicate that it is still running and to control the main while loop

        __obstacle = np.asarray(__obstacle)
        x_obs = __obstacle[:,0]
        y_obs = __obstacle[:,1]

        diff_x = abs(x_obs - self.x_ref)
        diff_y = abs(y_obs - self.y_ref)

        diff_angle = self.x_ref - self.theta
        max_dist = 200

        for j in range(0, len(y_obs)):

            if (diff_x > 20) and (diff_y > 20):  # obst not detected close by
                for i in range(j, j + 1):
                    if y_obs[j] > self.dist_dest:
                        if diff_angle == 0:
                            __orient_angle = self.theta
                        elif diff_angle > 0:
                            __orient_angle = self.x_ref + diff_angle
                        elif diff_angle < 0:
                            __orient_angle = self.x_ref - diff_angle
                        __obstacle_flag = True
                    else:
                        __obstacle_flag= False

                    # print("orient angle 1", orient_angle)

            elif (diff_x < 20) and (diff_y < 20):  # obs detected close by
                # set temp path
                alpha_temp = 90
                alpha_temp = np.radians(alpha_temp)
                # __orient_angle_det = self.theta + alpha_temp might not need this?

                diff_2 = alpha_temp - self.theta
                if y_obs[j] > self.dist_dest:
                    if diff_2 > 0:
                        __orient_angle = alpha_temp + diff_2
                    elif diff_2 < 0:
                        __orient_angle = alpha_temp - diff_2
                    __obstacle_flag = True
                else:
                    __obstacle_flag = False
                # print("orient angle 2", orient_angle2)
        pass

    def dist_dest(self):
        return math.sqrt(math.pow((self.x_dest - self.x_ref), 2) + math.pow(self.y_dest - self.y_ref), 2)

    def theta(self):
        return abs(math.radians(math.atan((self.y_dest - self.y_ref) / (self.x_dest - self.x_ref))))  # optimal travelling angle

    @property
    def orientation_angle(self):
        return self.__orient_angle

    #@property
    #def orientation_angle_det(self):
     #   return self.__orient_angle_det

    @property #this needs to be changed
    def obstacle_detected_flag(self):
        if not self.__obstacle_flag:

        return self.__obstacle_flag

    @property
    def running(self):
        while self.__running:

            # need to be fixed

            avoid_obs = self.avoid_obstacle(self, self.__obstacle, self.__obstacle_flag, __orient_angle)

        return

    @property
    def duration(self):
        return