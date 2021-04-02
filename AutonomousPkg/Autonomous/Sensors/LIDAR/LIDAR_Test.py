from Sensors.LIDAR.LIDAR_Interface import LIDAR_Interface
from Sensors.LIDAR.Utils import Ray, Stack
import time

lidar = LIDAR_Interface(loc="/dev/ttyUSB0")
def main():
    global lidar

    lidar.start()
    dur = time.perf_counter()

    try:
        while True:
            if lidar.recent_scan.__len__() > 0:
                scan = lidar.pop_recent_scan.copy()
                if scan.__len__() >= 360:
                    print("New Scan", time.perf_counter() - dur)
                    dur = time.perf_counter()

                for i in range(scan.__len__()):
                    s = Ray(copy=scan[i])
                   # print("Point:", i, "Theta:", s.theta, "Distance:", s.radius)
            else:
                #print("looping", lidar.recent_scan.__len__(), lidar.stack.length)
                time.sleep(1)

    except KeyboardInterrupt:
        lidar.exit_func()



if __name__ == '__main__':
    main()