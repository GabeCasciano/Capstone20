# Use this program to rigorously test the function of the IMU interface
# and the functionality of the sensor

from IMU_Interface import *
import time

if __name__ == "__main__":
    IMU = IMU_Interface(angle_sign=False)
    IMU.start()
    print(IMU.version , " : ", IMU.signed_angle)
    time.sleep(1)
    for i in range(0, 20):
        print(IMU.angular_pos)
        time.sleep(.5)

    IMU.do_calibration()
    for i in range(0, 10):
        print("calibrated",IMU.angular_pos)
        time.sleep(.5)

    IMU.set_angular_pos_rel()
    for i in range(0, 20):
        print("zero'ed", IMU.angular_pos)
        time.sleep(.5)
    IMU.stop_thread()
