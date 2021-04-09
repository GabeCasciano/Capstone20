from Autonomous.Sensors.Car.Car_Interface import Car_Interface
from Autonomous.Sensors.Car.PS4_Controller.PS4_Controller import PS4_Controller
import pygame

controller = PS4_Controller()


def main():
    global controller

    while True:
        pygame.event.pump()
        print("Left trigger", controller.Left_Trigger, "Right Trigger", controller.Right_Trigger)


if __name__ == '__main__':
    controller.start()
    try:
        main()
    except KeyboardInterrupt:
        print("Stopping")
        exit(1)