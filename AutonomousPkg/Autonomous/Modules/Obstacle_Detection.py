import numpy
import numpy as np
from Autonomous.Sensors.LIDAR import LIDAR_Interface,Utils
from threading import *

class Obstacle_Detection(Thread):

    def __init__(self, lidar: LIDAR_Interface.LIDAR_Interface, min_distance: int=0, max_distance: int=5000):

        self._lidar = lidar
        self._iter_scan = self._lidar.iter_scans(self.__samples_per_rev)
        self._lidar.min_distance = min_distance
        self._lidar.max_distance = max_distance

        super(Obstacle_Detection, self).__init__()

        self.__running = False
        self.__obstacle_flag = False
        self.__obstacle = np.array([0,0]) # this can be an np array if need be


    def stop_thread(self):
        self.__running = True

    def exit_func(self):
        self.stop_thread()
        self._lidar.exit_func()

    def zero_sensor(self):
        # needs an algorithm to find the center of the sensor
        pass

    def clear_obstacle_flag(self):
        self.__obstacle_flag = False
        self.__obstacle = (0, 0)  # reset the __obstacle var


    def range_filter(self, scans, min_distance, max_distance): # not sure if there needs to be a self here?
        x = scans[:, 1]
        for i in range(len(x)):
            if x[i] < min_distance:
                x[i] = 0
            elif x[i] > max_distance:
                x[i] = 0

        x = np.asarray(x)
        x = np.transpose(x)
        return x


    def segmentation(self, scans, seg_threshold): # not sure if there needs to be a self here?
        i = 1  # incremental num
        temp_val = scans[:, 1]
        segment = np.zeros((len(temp_val), 3))
        segment[:, 0] = temp_val
        x = [temp_val[len(temp_val) - 1]]
        np.asarray(x)
        temp_val = np.append(temp_val, x, axis=0)
        segment[:, 1] = abs(np.diff(temp_val, axis=0))
        # conditions where segment threshold > 20 mm, can be changed
        cond_1 = segment[:, 1] > seg_threshold
        check = np.where(cond_1, 2, 1)  # check where its true or false
        check = check.reshape(-1, 1)
        iter_seg = 1
        for k in range(len(check)):
            if check[k] == 2:  # true
                iter_seg = iter_seg + 1  # iterate to next segment
                check[k] = iter_seg
            elif check[k] == 1:  # false: diff between 2 distances is less than threshold
                check[k] = iter_seg  # same segment
        segment[:, 2] = check[:, 0]

        segment = segment[:, 2].reshape(-1, 1)

        return segment

    # class properties
    # @property
    # def obstacle_detected_flag(self):
    #     return self.__obstacle_flag

    @property
    def detected_obstacle(self): # returns [angle, dist, segment number]
        return self.__obstacle

    @property
    def max_distance(self):
        return self._lidar.max_distance

    @max_distance.setter
    def max_distance(self, distance):
        self._lidar.max_distance = distance

    @property
    def min_distance(self):
        return self._lidar.min_distance

    @min_distance.setter
    def min_distance(self, distance):
        self._lidar.min_distance = distance

    # thread functions
    def start(self) -> None:
        self.__running = True
        if not self._lidar.running:
            self._lidar.start()

    def run(self) -> None:
        while self.__running:
            # run the obstacle detection algorithm

            scan = next(self._iter_scan)
            __obstacle = np.array([(np.radians(point[1]), point[2]) for point in scan])
            x = self.range_filter(__obstacle, 0, 5000)
            __obstacle[:, 1] = x
            __obstacle = __obstacle[np.all(__obstacle != 0, axis=1)]  # removes rows with 0s
            segment = self.segmentation(__obstacle, 20)  # distance threshold function
            # add segment value column to offset array to plot
            __obstacle = np.append(__obstacle, segment, axis=1)

            pass


