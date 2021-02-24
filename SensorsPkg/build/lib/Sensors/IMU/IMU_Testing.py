# Use this program to rigorously test the function of the IMU interface
# and the functionality of the sensor

from IMU_Interface import IMU_Interface
import time

if __name__ == "__main__":
    IMU = IMU_Interface()
    IMU.start()
    time.sleep(1)
    while True:
        print(IMU.get_angular_orientation())
