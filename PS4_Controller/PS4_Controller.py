import pygame
from threading import *
import time

class PS4_Controller(Thread):

    _DEFAULT_PRESS =0
    _ON_PRESSED = 1
    _ON_RELASED = 2
    _X_AXIS = 1
    _Y_AXIS = 2
    _LEFT_STICK = 0
    _RIGHT_STICK = 2

    def __init__(self):
        super(PS4_Controller, self).__init__()
        self.running = True

        if pygame.joystick.get_count() > 0:
            pygame.display.init()
            pygame.joystick.init()
            self._joystick = pygame.joystick.Joystick(0)
            self._joystick.init()
        else:
            print("No joystick found")
            exit(1)

        self._buttons = []
        self._buttons_prev = []
        self._dpad = []
        self._dpad_prev = []

    def _check_button(self, type: int, button_num: int):
        if type == PS4_Controller._ON_PRESSED:
            return self._buttons_prev[button_num] != self._buttons[button_num] and self._buttons[button_num]
        elif type == PS4_Controller._ON_RELASED:
            return self._buttons_prev[button_num] != self._buttons[button_num] and not self._buttons[button_num]
        else:
            return self._buttons[button_num]

    def _check_dpad(self, type: int, direction: int):
        if type == PS4_Controller._ON_PRESSED:
            return self._dpad_prev[direction] != self._dpad[direction] and self._dpad[direction]
        elif type == PS4_Controller._ON_PRESSED:
            return self._dpad_prev[direction] != self._dpad[direction] and not self._dpad[direction]
        else:
            return self._dpad[direction]

    def _check_stick(self, direction: int, stick: int):
        if direction > 0:
            return self._joystick.get_axis(direction + stick - 1)
        else:
            return [self._joystick.get_axis(stick), self._joystick.get_axis(stick + 1)]

    def stop_thread(self):
        self.running = False

    # class properties
    @property
    def Left_Trigger(self):
        return self._joystick.get_axis(5)

    @property
    def Right_Trigger(self):
        return self._joystick.get_axis(4)

    @property
    def Left_Stick(self, axis: int = 0):
        return self._check_stick(axis, PS4_Controller._LEFT_STICK)

    @property
    def Right_Stick(self, axis: int = 0):
        return self._check_stick(axis, PS4_Controller._RIGHT_STICK)

    @property
    def Up(self, type: int = 0):
        return self._check_dpad(type, 0)

    @property
    def Down(self, type: int = 0):
        return self._check_dpad(type, 1)

    @property
    def Left(self, type: int = 0):
        return self._check_dpad(type, 2)

    @property
    def Right(self, type: int = 0):
        return self._check_dpad(type, 3)

    @property
    def Cross(self, type: int = 0):
        return self._check_button(type, 0)

    @property
    def Circle(self, type: int = 0):
        return self._check_button(type, 1)

    @property
    def Square(self, type: int = 0):
        return self._check_button(type, 2)

    @property
    def Triangle(self, type: int = 0):
        return self._check_button(type, 3)

    @property
    def Left_Bumper(self, type: int = 0):
        return self._check_button(type, 4)

    @property
    def Right_Bumper(self, type: int = 0):
        return self._check_button(type, 5)

    @property
    def L3(self, type: int = 0):
        return self._check_button(type, 10)

    @property
    def R3(self, type: int = 0):
        return self._check_button(type, 11)

    @property
    def Touch_Pad(self, type: int = 0):
        return self._check_button(type, 13)

    @property
    def PS(self, type: int = 0):
        return self._check_button(type, 12)

    @property
    def Share(self, type: int = 0):
        return self._check_button(type, 8)

    @property
    def Options(self, type: int = 0):
        return self._check_button(type, 9)


    @property
    def On_Pressed(self):
        return PS4_Controller._ON_PRESSED

    @property
    def On_Released(self):
        return PS4_Controller._ON_RELASED

    @property
    def X_Axis(self):
        return PS4_Controller._X_AXIS

    @property
    def Y_Axis(self):
        return PS4_Controller._Y_AXIS

    # Thread functions
    def start(self) -> None:
        self.running = True

    def run(self) -> None:
        while self.running:
            pygame.event.pump()

            self._buttons_prev = self._buttons.copy()
            self._dpad_prev = self._dpad.copy()

            self._buttons = []
            for i in range(self._joystick.get_numbuttons()):
                self._buttons.append(self._joystick.get_button(i))

            self._dpad = []
            temp = self._joystick.get_hat(0)

            if temp[1] == 0:
                self._dpad.append(False)
                self._dpad.append(False)
            elif temp[1] == 1:
                self._dpad.append(True)
                self._dpad.append(False)
            elif temp[1] == -1:
                self._dpad.append(False)
                self._dpad.append(True)

            if temp[0] == 0:
                self._dpad.append(False)
                self._dpad.append(False)
            elif temp[0] == 1:
                self._dpad.append(False)
                self._dpad.append(True)
            elif temp[0] == -1:
                self._dpad.append(True)
                self._dpad.append(False)