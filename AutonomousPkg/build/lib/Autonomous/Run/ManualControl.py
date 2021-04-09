from Autonomous.Sensors.Car.PS4_Controller.PS4_Controller import PS4_Controller
from Autonomous.Sensors.Car.Car_Interface import Car_Interface

import pygame
import tkinter as tk
from threading import *


class CarJoy(Thread):
    def __init__(self, car: Car_Interface, controller: PS4_Controller):
        super(CarJoy, self).__init__()
        self.car = car
        self.controller = controller
        self.running = False

    def stop_thread(self):
        self.car.motor_speed = 0
        self.car.steering_angle = 0
        self.running = False

    def start(self) -> None:
        print("Starting controller")

        self.running = True
        if not self.car.running:
            self.car.start()
        if not self.controller.running:
            self.controller.start()

        super(CarJoy, self).start()

    def exit_car(self):
        self.car._exit_cmd()
        exit(0)

    def connect_to_car(self):
        if not self.car.running:
            self.car.start()

    def run(self) -> None:
        print("Started loop")
        while self.running:
            pygame.event.pump()
            self.car.motor_speed = (self.controller.Right_Trigger + 1) * 64
            self.car.steering_angle = self.controller.Left_Stick_X * 30
            #self.car.left_led = self.controller.Left_Bumper
            #self.car.right_led = self.controller.Right_Bumper
            print("Speed:", self.controller.Left_Trigger,"steering:", self.car.steering_angle)


class ManualWindow(tk.Frame):

    def __init__(self, _joy:CarJoy, master=None):
        super(ManualWindow, self).__init__()
        self.master = master
        self.pack()
        self._joy_thread = _joy

        self.en_btn = tk.Button(self, text="Enable", command=self._enable_car)
        self.en_btn.pack()

        self.dis_btn = tk.Button(self, text="Disable", command=self._stop_car)
        self.dis_btn.pack()

        self.connect_btn = tk.Button(self, text="Connect", command=self._connect_to_car)
        self.connect_btn.pack()

        self.kill_btn = tk.Button(self, text="Kill", command=self._exit_car)
        self.kill_btn.pack()

    def _enable_car(self):
        self._joy_thread.start()

    def _stop_car(self):
        self._joy_thread.stop_thread()

    def _exit_car(self):
        self._joy_thread.exit_car()

    def _connect_to_car(self):
        self._joy_thread.connect_to_car()

if __name__ == "__main__":

    controller = PS4_Controller()
    car = Car_Interface(loc="/dev/ttyUSB0")
    root = tk.Tk()
    joy = CarJoy(car, controller)
    window = ManualWindow(joy)
    window.mainloop()
