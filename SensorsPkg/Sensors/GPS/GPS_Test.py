# Use this python file rigorously test all fo the GPS interface functions
# and the functionality of the GPS itself

from Sensors.GPS.GPS_Interface import *

if __name__ == '__main__':

    gps = GPS_Interface()
    gps.start()
    while True:
        print(gps.get_position())