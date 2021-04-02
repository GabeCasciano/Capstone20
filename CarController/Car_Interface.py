from threading import *
from serial import *
import time


class Car_Interface(Thread):

    _MAX_STEERING_ANGLE = 100
    _MIN_STEERING_ANGLE = 0
    _MID_STEERING_ANGLE = 50

    _MAX_CAR_SPEED = 255
    _MIN_CAR_SPEED = -255

    def __init__(self, loc: str = "/dev/ttyTMS1", baud: int = 9600, motor_offset: int = 0, steering_offset: int = 0):

        super(Car_Interface, self).__init__()

        self._motor_speed = 0
        self._steering_angle = 0

        self._motor_offset = motor_offset
        self._steering_angle_offset = steering_offset

        self._cs_battery = []
        self._m_battery = []

        self._left_led = False
        self._right_led = False

        self.__running = False

        self._serial = Serial()
        self._serial.port = loc
        self._serial.baudrate = baud

    def stop_thread(self):
        self.__running = False
        self._serial.close()

    def start(self) -> None:
        self.__running = True

    def run(self) -> None:
        self._serial.open()
        self._do_handshake()

        while self.__running:
            pass
            # basically this is just to poll the cars data

    def _do_handshake(self):
        pass

    def _send_motor_command(self):
        pass

    def update_motor_command(self, speed: int, steering: int):
        pass

    def _poll_car_data(self):
        pass

    def _set_car_parameters(self, param_number: int, param):
        pass

    def _enable_lights(self):
        pass
