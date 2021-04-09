from Autonomous.Sensors.IMU.IMU_Interface import IMU_Interface
from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface
from Autonomous.Sensors.Car.Car_Interface import Car_Interface
from Autonomous.Modules.Sensor_Fusion import Sensor_Fusion

from math import cos, sin, radians
import time


def main():
    car = Car_Interface(loc="/dev/ttyUSB1")
    imu = IMU_Interface(loc="/dev/ttyUSB0")
    gps = GPS_Interface(loc="/dev/ttyACM0")

    sf = Sensor_Fusion(IMU=imu, GPS=gps)

    car.start()
    sf.start()

    fk_lat = 43.180208
    fk_long = -79.790125

    lat = float(input("Destination lat"))
    long = float(input("Destination long"))

    time.sleep(1) # allow everything to start

    #pp = Path_Planning(long, lat, sf)

    while True:
        #dist = GPS_Interface.haversin(sf.gps_vector, [lat, long])
        #angle = GPS_Interface.bearing_to(sf.gps_vector, [lat, long])

        dist = GPS_Interface.haversin([fk_lat, fk_long], [lat, long])
        angle = GPS_Interface.bearing_to([fk_lat, fk_long], [lat, long])

        # convert and compare the correction vector to the car direction
        # turn until theta = 0, then drive towards the point

        dif_angle = angle - sf.orientation

        print("Distance:", dist, "angle:", angle, "error:", dif_angle)

        if dist > 3:  # 3m is the tolerance of the gps
            if abs(dif_angle) > 1:  # 1 degree of tolerance (car can't steer to that accuracy anyways)
                car.steering_angle = dif_angle
                car.motor_speed = 50
            else:
                # drive straight
                car.steering_angle = 0
                car.motor_speed = 100
        else:
            print("Done")
            car.motor_speed = 0
            car.stop_thread()
            sf.stop_thread()
            return




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")


