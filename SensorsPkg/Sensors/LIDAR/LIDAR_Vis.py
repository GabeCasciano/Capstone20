from .LIDAR_Interface import LIDAR_Interface
import os
from math import cos, sin, pi, floor
import pygame

lidar = LIDAR_Interface(loc="/dev/USB1")
lidar.start()

pygame.init()

screen