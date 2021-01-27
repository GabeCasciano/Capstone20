from IMU_Interface import IMU_Interface
import time

if __name__ == "__main__":
    IMU = IMU_Interface()
    IMU.start()
    time.sleep(1)
    while True:
        print(IMU.get_linear_acceleration())