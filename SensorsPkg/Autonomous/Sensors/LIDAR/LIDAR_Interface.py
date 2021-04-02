# https://github.com/GabeCasciano/Capstone20/blob/Obstacle_Det/Obstacle_Det/main.py
# https://github.com/SkoltechRobotics/rplidar/blob/master/rplidar.py

from threading import *
from rplidar import RPLidar
import atexit
from Utils import *

# Samples per revolution is 360, the sensor will increase its sample rate to maintain this
# the best that it can. Ex. slower speed = slower sample rate, higher speed = higher sample rate

class LIDAR_Interface(Thread):

    # These are all in Hz
    _MAX_SCAN_RATE = 10
    _MIN_SCAN_RATE = 0
    _MAX_SCAN_PWM = 1023
    _MIN_SCAN_PWM = 0
    _DEFAULT_SCAN_RATE = 5.5
    _GENERATOR_BUFF_SIZE = 500
    _ANGULAR_TOLERANCE = 2

    def __init__(self, loc: str = "/dev/ttyUSB1", sample_rate: float = 4000, scan_rate: float = 5.5, stack_depth:int = 10):
        self.__lidar = RPLidar(port=loc)
        super(LIDAR_Interface, self).__init__()

        self.__min_parsable = 5
        self.__sample_rate = sample_rate
        self.__scan_rate = scan_rate
        self.__samples_per_rev = LIDAR_Interface._GENERATOR_BUFF_SIZE # this may change after testing

        self.__iter = self.__lidar.iter_scans(self.__samples_per_rev)

        self.__stack = Stack(stack_depth)
        self.__current_scan = []
        self.__prev_scan = []

        self._max_distance = 5000
        self._min_distance = 0

        self.running = True

        atexit.register(self.exit_func)

    # control functions
    def stop_thread(self):
        self.running = False

    def exit_func(self):
        self.stop_thread()
        self.stop_motor()
        self.stop_sensor()
        self.__lidar.disconnect()

    def stop_sensor(self):
        self.__lidar.stop()

    def stop_motor(self):
        self.__lidar.stop_motor()

    def reset_sensor(self):
        self.__lidar.reset()
        self.__lidar.clear_input()

    def start_motor(self):
        self.__lidar.start_motor()

    # properties
    @property
    def max_distance(self):
        return self._max_distance

    @max_distance.setter
    def max_distance(self, distance: int):
        if distance > self._min_distance:
            if distance < 15:
                self._max_distance = distance

    @property
    def min_distance(self):
        return self._min_distance

    @min_distance.setter
    def min_distance(self, distance: int):
        if distance >= 0:
            if distance < self._max_distance:
                self._min_distance = distance

    @property
    def sensor_health(self):
        return self.__lidar.get_health()

    @property
    def sensor_info(self):
        return self.__lidar.get_info()

    @property
    def sample_rate(self):
        return self.__sample_rate

    @property
    def scan_rate(self):
        return self.__scan_rate

    @scan_rate.setter
    def scan_rate(self, value: float):
        if LIDAR_Interface._MAX_SCAN_RATE >= value >= LIDAR_Interface._MIN_SCAN_RATE:
            self.__scan_rate = value
            self.__sample_rate = LIDAR_Interface._GENERATOR_BUFF_SIZE * self.__scan_rate
            self._set_scan_rate()

    @property
    def pop_recent_scan(self) -> list:
        if self.__stack.length > 0:
            return self.__stack.pop()
        return list()

    @property
    def recent_scan(self) -> list:
        if self.__stack.length > 0:
            return self.__stack.top
        return list()

    @property
    def stack(self) -> Stack:
        return self.__stack

    # conversion function
    @staticmethod
    def _map(x: float, from_min: float, from_max: float, to_min: float, to_max: float) -> float:
        return (x - from_min) * (to_max - to_min) / ((from_max - from_min) + to_min)

    # Motor control functions
    def _set_scan_rate(self):
        self.__lidar.set_pwm(self._map(self.__scan_rate, LIDAR_Interface._MIN_SCAN_RATE, LIDAR_Interface._MAX_SCAN_RATE,
                                       LIDAR_Interface._MIN_SCAN_PWM, LIDAR_Interface._MAX_SCAN_PWM))

    # thread function
    def start(self) -> None:
        super(LIDAR_Interface, self).start()
        self.running = True

    def run(self) -> None:
        while self.running:
            # iter must produce a full rotation (360 points) before we can use it
            #_scan = self.__lidar.iter_scans(min_len=self.__samples_per_rev)

            if self.__iter.__sizeof__() > 0:
                _scan = next(self.__iter)
                for scan in _scan:
                    current = Ray(scan[2], scan[1], scan[0])
                    if current.radius > self._min_distance:
                        if current.radius < self._max_distance:
                            self.__current_scan.append(current)

                    # if the current scan has the total points for a rotation we can consume it and reset the current scan
                    if self.__current_scan.__len__() >= 360:
                        self.__stack.push(self.__current_scan.copy())
                        self.__current_scan.clear()

        self.__lidar.stop()
        self.__lidar.stop_motor()
        self.__lidar.disconnect()

