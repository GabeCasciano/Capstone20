from .GPS import GPS_Interface
from .IMU import IMU_Interface
from .LIDAR import LIDAR_Interface


# Sensors should be initialized before being passed into Thread handler
# thread handler should be used to abstract the threading functionality into easier to use controls

class SensorThreadHandler:

    def __init__(self, imu: IMU_Interface = None, gps: GPS_Interface = None, lidar: LIDAR_Interface = None):
        self.__sensors = []
        if imu is not None:
            self.__sensors.append(imu)
        if gps is not None:
            self.__sensors.append(gps)
        if lidar is not None:
            self.__sensors.append(lidar)

    def start_available(self):
        for s in self.__sensors:
            s.start()

    def stop_available(self):
        for s in self.__sensors:
            s.stop_thread()

    def stop_imu(self):
        for s in self.__sensors:
            if type(s) == IMU_Interface:
                s.stop_thread()

    def stop_gps(self):
        for s in self.__sensors:
            if type(s) == GPS_Interface:
                s.stop_thread()

    def stop_lidar(self):
        for s in self.__sensors:
            if type(s) == LIDAR_Interface:
                s.stop_thread()

    def start_imu(self):
        for s in self.__sensors:
            if type(s) == IMU_Interface:
                s.start()

    def start_gps(self):
        for s in self.__sensors:
            if type(s) == GPS_Interface:
                s.start()

    def start_lidar(self):
        for s in self.__sensors:
            if type(s) == LIDAR_Interface:
                s.start()
