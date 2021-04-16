from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface
from Autonomous.Sensors.IMU.IMU_Interface import IMU_Interface
from Autonomous.Sensors.Car.Car_Interface import Car_Interface
from Autonomous.Sensors.LIDAR.LIDAR_Interface import LIDAR_Interface

from Autonomous.Modules.Path_Planning import *
from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion
from Autonomous.Modules.Obstacle_Detection import *
from Autonomous.Modules.Obstacle_Avoidance import *

import time
from math import cos, sin, tan, sqrt, radians


def main():
    car = Car_Interface(loc="/dev/ttyUSB0")
    imu = IMU_Interface(loc="/dev/ttyUSB1")
    gps = GPS_Interface(loc="/dev/ttyACM0")
    lidar = LIDAR_Interface(loc="/dev/ttyUSB2")

    sf = Sensor_Fusion(IMU=imu, GPS=gps)
    obj = Obstacle_Detection(lidar=lidar)

    car.start()
    sf.start()
    obj.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("stopping")