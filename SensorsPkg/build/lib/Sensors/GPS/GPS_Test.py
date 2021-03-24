# Use this python file rigorously test all fo the GPS interface functions
# and the functionality of the GPS itself

from GPS_Interface import *
from time import *

if __name__ == '__main__':

    gps = GPS_Interface()
    gps.start()
    for i in range(0,19):
        print(gps.position, gps.error_flag)
        sleep(.5)
    gps.stop_thread()
    exit(0)