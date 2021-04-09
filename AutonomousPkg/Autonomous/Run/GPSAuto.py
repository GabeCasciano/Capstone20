from Autonomous.Sensors.GPS.GPS_Interface import GPS_Interface
from Autonomous.Sensors.Car.Car_Interface import Car_Interface
from Autonomous.Modules.Path_Planning import *




def main():
    global lat, long

    car = Car_Interface(loc="/dev/ttyUSB0")
    gps = GPS_Interface(loc="/dev/ttyACM0")
    path_plan = Path_Planning(gps.latitude, gps.longitude, lat, long)




if __name__ == '__main__':
    lat = input("Destination lat:")
    long = input("Destination long:")

    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")
