from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface
from Autonomous.Sensors.IMU.IMU_Interface import IMU_Interface
from Autonomous.Sensors.Car.Car_Interface import Car_Interface

from Autonomous.Modules.Path_Planning import *
from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion

import time
from math import cos, sin, tan, sqrt, radians

def main():
    car = Car_Interface(loc="/dev/ttyUSB2")
    imu = IMU_Interface(loc="/dev/ttyUSB0")
    gps = GPS_Interface(loc="/dev/ttyACM0")

    sf = Sensor_Fusion(IMU=imu, GPS=gps)

    imu.start()
    gps.start()
    car.start()
    sf.start()

    time.sleep(1)

    lat = float(input("Destination lat:"))
    long = float(input("Destination long:"))

    path = Path_Planning(long, lat, sf)
    dist = GPS_Interface.haversin(sf.gps_vector, [lat, long])  # calc distance remaining

    while True:
        correction = path.follow_path()  # calculate the correction vector

        angle = tan(correction[1]/correction[0])  # convert cartesian into an angle

        sf_mag = sqrt(sf.position_x ** 2 + sf.position_y ** 2) # convert the sf position into cylindrical coords

        dif_angle = angle - sf.orientation  # calculate the angular difference
        dif_dist = dist - sf_mag  # calculate the linear difference

        # output is proportional to dif calcs, (props, have saturation implemented)
        car.steering_angle = dif_angle
        car.motor_speed = dif_dist

        print("dist:", dif_dist, "angle:", dif_angle, "correction vector:", correction)

        if dif_dist < 1:
            print("Reached destination")
            car.stop_thread()
            sf.stop_thread()
            return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")
        exit(1)