from serial import Serial, tools
from threading import *
from math import radians, cos, sin, asin, atan, sqrt
from time import *
from datetime import datetime
import atexit


class GPS_Interface(Thread):

    _NMEA_VALID_COMMANDS = ["GPGLL", "GPRMC", "GPTRF", "GPVBW", "GPVTG"]
    KNOTS_TO_KM = 1.852
    RADIUS_OF_EARTH = 6371

    def __init__(self, loc: str = '/dev/ttyACM0', baud: int = 4800):
        self.__gps_serial = Serial()
        self.__gps_serial.port = loc
        self.__gps_serial.baudrate = baud

        super(GPS_Interface, self).__init__()

        self._latitude = 0
        self._longitude = 0
        self._altitude = 0
        self._ground_speed = 0

        self._latitude_rel = 0
        self._longitude_rel = 0

        self._gps_time = 0
        self._prev_gps_time = 0

        self.running = True
        self.error_flag = False
        self._new_data_flag = False

        self._current_time = 0
        self._prev_time = 0
        self._sample_rate = 0

        atexit.register(self.exit_func)

    # Control Functions
    def stop_thread(self):
        self.running = False

    def exit_func(self):
        self.__gps_serial.close()

    def __do_new_data_flag(self):
        self._current_time = perf_counter()
        if self._gps_time == self._prev_gps_time:
            self._new_data_flag = False
            return

        if self.position == [0.0, 0.0] or self.position == [float("NaN"), float("NaN")]: # not initialized or started
            self._new_data_flag = False
            return

        self._sample_rate = self._current_time - self._prev_time
        self._prev_time = self._current_time
        self._prev_gps_time = self._gps_time
        self._new_data_flag = True

    # parse functions
    def __parse_time(self, _time: str):
        time_string = list(_time)
        if time_string.__len__() >= 9:
            hour = str(time_string[0] + time_string[1])
            minute = str(time_string[2] + time_string[3])
            second = str(time_string[4] + time_string[5])
            self._gps_time = datetime(year = datetime.now().year , month=datetime.now().month, day = datetime.now().day, hour=int(hour), minute=int(minute), second=int(second))

    def __parse_GGA(self, data: list):
        self.__parse_time(data[0])
        self._latitude = self.convert_min_to_decimal(data[1], data[2]) if (data[1] != "" or data[2] != "") else float("NaN")
        self._longitude = self.convert_min_to_decimal(data[3], data[4]) if (data[3] != "" or data[4] != "") else float("NaN")
        self._altitude = float(data[8]) if (data[8] != "") else float("NaN")
        self.__do_new_data_flag()

    def __parse_GGL(self, data: list):
        self.__parse_time(data[4])
        self._latitude = self.convert_min_to_decimal(data[0], data[1])
        self._longitude = self.convert_min_to_decimal(data[2], data[3])
        self.__do_new_data_flag()

    def __parse_RMA(self, data: list):
        if data[0] == 'A':
            self._latitude = self.convert_min_to_decimal(data[1], data[2]) if (data[1] != "" or data[2] != "") else float("NaN")
            self._longitude = self.convert_min_to_decimal(data[3], data[4]) if (data[3] != "" or data[4] != "") else float("NaN")
            self._ground_speed = float(data[7]) * GPS_Interface.KNOTS_TO_KM if (data[7] != "") else float("NaN")
            self.__do_new_data_flag()

    def __parse_RMC(self, data: list):
        self.__parse_time(data[0])
        self._latitude = self.convert_min_to_decimal(data[2], data[3]) if (data[2] != "" or data[3] != "") else float("NaN")
        self._longitude = self.convert_min_to_decimal(data[4], data[5]) if (data[4] != "" or data[5] != "") else float("NaN")
        self._ground_speed = float(data[6]) * GPS_Interface.KNOTS_TO_KM if (data[6] != "") else float("NaN")
        self.__do_new_data_flag()

    def __parse_TRF(self, data: list):
        self.__parse_time(data[0])
        self._latitude = self.convert_min_to_decimal(data[2], data[3]) if (data[2] != "" or data[3] != "") else float("NaN")
        self._longitude = self.convert_min_to_decimal(data[4], data[5]) if (data[4] != "" or data[5] != "") else float("NaN")
        self.__do_new_data_flag()

    # run funtions
    def run(self) -> None:
        self.__gps_serial.open()

        for i in range(0, 7): # first handful of lines are bs
            self.__gps_serial.readline()

        while self.running:
            data = str(self.__gps_serial.readline()).replace("'", "").replace("b", "").split(",")
            command = data.pop(0)
            if data[0] != "":
                if command == "$GPGGA":
                    self.__parse_GGA(data)
                elif command == "$GPGLL":
                    self.__parse_GGL(data)
                elif command == "$GPRMC":
                    self.__parse_RMC(data)
                elif command == "$GPTRF":
                    self.__parse_TRF(data)
            else:
                self.error_flag = True

        self.__gps_serial.close()

    # get functions
    @property
    def position(self) -> list:
        return [self._latitude, self._longitude]

    @property
    def latitude(self) -> float:
        return self._latitude

    @property
    def longitude(self) -> float:
        return self._longitude

    @property
    def new_data_flag(self):
        return self._new_data_flag

    @property
    def ground_speed(self) -> float:
        return self._ground_speed

    @property
    def sample_rate(self) -> float:
        return self._sample_rate

    @property
    def gps_time(self):
        return self._gps_time

    # math functions
    @staticmethod
    def haversin(start: list, goal: list) -> float:
        lat1, lon1, lat2, lon2 = map(radians, [start[0], start[1], goal[0], goal[1]])

        delta_lat = lat1-lat2
        delta_lon = lon1-lon2

        a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2)
        c = 2 * asin(sqrt(a))
        return c * GPS_Interface.RADIUS_OF_EARTH

    @staticmethod
    def bearing_to(start: list, goal: list) -> float:
        lat, lon = map(radians, [goal[0] - start[0], goal[1] - start[1]])
        return atan(lon/lat)

    # conversion functions
    @staticmethod
    def convert_min_to_decimal(position: str, direction: chr) -> float:
        try:
            temp = position.split(".")
            before = list(temp[0])

            if before[0] == '0':
                before.remove('0')

            degrees = float(before[0] + before[1])
            minutes = float(before[2] + before[3] + ',' + temp[1])
        except:
            degrees = 0
            minutes = 0

            return float("NaN")

        return (1 if (direction == 'N' or direction == 'E') else -1) * (degrees + (minutes/60))

