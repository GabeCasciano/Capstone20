import serial
from threading import *

class Car_Interface(Thread):

    _LLED_CMD = 'L'
    _RLED_CMD = 'R'
    _BOOL_T = 'T'
    _BOOL_F = 'F'

    _PACKET_SIZE = 64

    def __init__(self, loc: str='/dev/ttyUB0', baud: int=9600):

        self.__serial = serial.Serial()
        self.__serial.port = loc
        self.__serial.baudrate = baud

        super(Car_Interface, self).__init__()

        self.__running = False

        self._left_led = False
        self._right_led = False

    def stop_thread(self):
        self.__running = False

    @property
    def running(self):
        return self.__running

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
