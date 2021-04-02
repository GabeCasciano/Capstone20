from Sensors.LIDAR.LIDAR_Interface import LIDAR_Interface
from Sensors.LIDAR.Utils import Ray, Stack
from math import cos, sin, pi, floor
import pygame
import time

screen_x = 400
screen_y = 400
lidar = LIDAR_Interface(loc="/dev/ttyUSB0")


def main():
    global screen_y, screen_x, lidar

    lidar.start()

    pygame.init()

    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.mouse.set_visible(False)
    screen.fill(pygame.Color(0,0,0))
    dur = time.perf_counter()

    try:
        while True:
            current_scan = lidar.pop_recent_scan
            if current_scan is not None:
                for i in range(current_scan.__len__()):
                    rads = current_scan[i].theta * pi / 180.0
                    x = current_scan[i].radius/25 * cos(rads)
                    y = current_scan[i].radius/25 * sin(rads)
                    point = (int(x + (screen_x / 2)), int(y + (screen_y/2)))
                    screen.set_at(point, pygame.Color(255,255,255))
                    #print("Point", i)
                    #print("Angle:", current_scan[i].theta, "Radius:", current_scan[i].radius)
                pygame.display.update()
                print("time", time.perf_counter() - dur)
                dur = time.perf_counter()

    except KeyboardInterrupt:
        lidar.stop_thread()
        lidar.stop_motor()
        lidar.stop_sensor()
        lidar.exit_func()


if __name__ == "__main__":
    main()
