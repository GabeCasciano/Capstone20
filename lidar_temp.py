from rplidar import *

if __name__ == "__main__":
    lidar = RPLidar(port="/dev/ttyUSB0")


    while True:

        _iter = lidar.iter_scans()
        if _iter.__sizeof__() > 0:
            print("new scan")

