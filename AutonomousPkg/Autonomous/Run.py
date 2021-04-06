# use this as the main thread
from threading import *
import time

from Autonomous.Sensors.LIDAR.Utils import Ray, Stack
from Autonomous.Sensors.LIDAR.LIDAR_Interface import  LIDAR_Interface
from Autonomous.Sensors.IMU.IMU_Interface import IMU_Interface
from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface
from Autonomous.Sensors.Car.Car_Interface import Car_Interface

lidar = LIDAR_Interface(loc="/dev/ttyUSB0")
imu = IMU_Interface(loc="/dev/ttyUSB1")
gps = GPS_Interface(loc="/dev/ttyACM0")
car = Car_Interface(loc="/dev/ttySM0")  # need to double check this on the jetson nano


if __name__ == '__main__':
    pass