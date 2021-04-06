from Autonomous.Sensors.LIDAR import LIDAR_Interface, Utils
from threading import *

class Obstacle_Detection(Thread):

    def __init__(self, lidar: LIDAR_Interface.LIDAR_Interface, min_distance: int=0, max_distance: int=5000):
        self._lidar = lidar
        self._lidar.min_distance = min_distance
        self._lidar.max_distance = max_distance

        super(Obstacle_Detection, self).__init__()

        self.__running = False
        self.__obstacle_flag = False
        self.__obstacle = (0, 0) # this can be an np array if need be

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

    # class properties
    @property
    def obstacle_detected_flag(self):
        return self.__obstacle_flag

    @property
    def detected_obstacle(self): # returns the closest obstacle (position, angle)
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
            pass


