import serial
from threading import *

class Car_Interface(Thread):

    _LLED_CMD = 'L'
    _RLED_CMD = 'R'
    _M_CMD = 'M'
    _S_CMD = 'S'
    _BOOL_T = 'T'
    _BOOL_F = 'F'

    _PACKET_SIZE = 64

    _MAX_SPEED = 128
    _MIN_SPEED = -128

    _MAX_ANGLE = 30
    _MIN_ANGLE = -30

    def __init__(self, loc: str='/dev/ttyUSB0', baud: int=9600):

        self.__serial = serial.Serial()
        self.__serial.port = loc
        self.__serial.baudrate = baud

        super(Car_Interface, self).__init__()

        self.__running = False

        self._left_led = False
        self._right_led = False

        self.__motor_speed = 0
        self.__steering_angle = 0

    def stop_thread(self):
        self.__running = False

    @property
    def running(self):
        return self.__running

    @property
    def steering_angle(self):
        return self.__steering_angle

    @steering_angle.setter
    def steering_angle(self, angle: int):
        self.__steering_angle = angle
        if angle >= Car_Interface._MAX_ANGLE:
            self.__steering_angle = Car_Interface._MAX_ANGLE
        if angle <= Car_Interface._MIN_ANGLE:
            self.__steering_angle = Car_Interface._MIN_SPEED

        txt = Car_Interface._S_CMD + str(self.__steering_angle) + self._BOOL_T
        self.__serial.write(txt.encode(encoding="ASCII"))

    @property
    def motor_speed(self):
        return self.__motor_speed

    @motor_speed.setter
    def motor_speed(self, speed: int):
        self.__motor_speed = speed
        if Car_Interface._MIN_SPEED >= speed:
            self.__motor_speed = Car_Interface._MIN_SPEED
        if Car_Interface._MAX_SPEED <= speed:
            self.__motor_speed = Car_Interface._MAX_SPEED

        txt = Car_Interface._M_CMD + str(self.__motor_speed) + self._BOOL_F
        self.__serial.write(txt.encode(encoding="ASCII"))

    @property
    def left_led(self) -> bool:
        return self._left_led

    @left_led.setter
    def left_led(self, state: bool):
        self._left_led = state
        txt = Car_Interface._LLED_CMD

        if self._left_led:
            txt += Car_Interface._BOOL_T
        else:
            txt += Car_Interface._BOOL_F

        if self.__running:
            self.__serial.write(txt.encode(encoding="ASCII"))

    @property
    def right_led(self) -> bool:
        return self._right_led

    @right_led.setter
    def right_led(self, state: bool):
        self._right_led = state
        txt = Car_Interface._RLED_CMD

        if self._right_led:
            txt += Car_Interface._BOOL_T
        else:
            txt += Car_Interface._BOOL_F

        if self.__running:
            self.__serial.write(txt.encode(encoding="ASCII"))

    def _do_handshake(self):
        txt = 'Gc'
        while not self.__serial.writable():
            pass
        self.__serial.write(txt.encode(encoding='ASCII'))

    def start(self) -> None:
        super(Car_Interface, self).start()
        self.__serial.open()
        self.__running = True
        self._do_handshake()

    def run(self) -> None:
        while self.__running:
            if self.__serial.readable():
                print(self.__serial.read(Car_Interface._PACKET_SIZE))
