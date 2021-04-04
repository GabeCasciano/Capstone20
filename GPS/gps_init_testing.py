import time
from GPS.GPS_Interface import GPS_Interface


if __name__ == "__main__":

    gps = GPS_Interface()
    gps.start()

    time.sleep(1)

    print(gps.latitude, ", ", gps.longitude)

    gps.running = False
    gps.join()