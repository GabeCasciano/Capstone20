# Use this python file rigorously test all fo the GPS interface functions
# and the functionality of the GPS itself

from Sensors.GPS.GPS_Interface import *

if __name__ == '__main__':

    gps = GPS_Interface()
    gps.start()
    for i in range(0,19):
        print(gps.get_position())
    gps.stop_thread()
    exit(0)