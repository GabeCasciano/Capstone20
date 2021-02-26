# use this library to ensure that the system can reach all of the libraries
# and that they have been installed correctly on the system

from Sensors.GPS.GPS_Interface import GPS_Interface
from Sensors.IMU
if __name__ == "__main__":
    gps = GPS_Interface()
    gps.start()
    for i in range(0,10):
        print(gps.get_latitude())