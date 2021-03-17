# https://github.com/GabeCasciano/Capstone20/blob/Obstacle_Det/Obstacle_Det/main.py
# https://github.com/SkoltechRobotics/rplidar/blob/master/rplidar.py

from threading import *
from time import *
from rplidar import RPLidar
import atexit

class Ray:
    def __init__(self, radius: float=None, theta: float=None, quality: float=None):
        self.__radius = radius
        self.__theta = theta
        self.__quality = quality

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        if value > 0:
            self.__radius = value

    @property
    def theta(self) -> float:
        return self.__theta

    @theta.setter
    def theta(self, value: float):
        if value > 0:
            self.__theta = value

    @property
    def quality(self) -> float:
        return self.__quality

    @quality.setter
    def quality(self, value: float):
        if value > 0:
            self.__quality = value

    @property
    def data(self) -> list:
        return [self.__radius, self.__theta]

class LIDAR_Interface(Thread):

    def __init__(self, loc: str = "/dev/ttyUSB1", sample_rate: float = 4000, rotation_rate: float = 5.5):
        self.__lidar = RPLidar(loc)

        self.__min_parsable = 5
        self.__sample_rate = sample_rate
        self.__rotation_rate = rotation_rate
        self.__samples_per_rotation = self.__sample_rate/self.__rotation_rate
        self.__lidar_iter = self.__lidar.iter_scans(int(self.__samples_per_rotation), self.__min_parsable)


        self.__current_scan = []
        self.__prev_scan = []

        self.running = True


    def run(self) -> None:
        pass

