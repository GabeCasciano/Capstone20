# Gabriel Casciano, Feb 7, 2021

# Capestone 2020-2021

# This library is used to interface with the USB GPS to interface over the serial bus.
# This interface is multithreaded so it can run simultaneous to other interfaces and other
# system functionality

from serial import Serial
from serial import tools
from threading import *
from math import radians, cos, sin, asin, atan, sqrt
import time
import atexit

class GPS_Interface(Thread):

    data_queue = []
    NMEA_VALID_COMMANDS = ["GPGLL", "GPRMC", "GPTRF", "GPVBW", "GPVTG"]
    KNOTS_TO_KM = 1.852
    RADIUS_OF_EARTH = 6371

    def __init__(self, loc: str = '/dev/ttyACM0', baud: int = 4800):
        self.gps_serial = Serial()
        self.gps_serial.port = loc
        self.gps_serial.baudrate = baud

        super(GPS_Interface, self).__init__()

        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.ground_speed = 0

        self.relative_latitude = 0
        self.relative_longitude = 0

        self.running = True

        self.current_time = 0
        self.prev_time = 0
        self.sample_rate = 0

        atexit.register(self.do_exit)

    # --- Parsing thread ---

    def run(self) -> None:
        self.gps_serial.open()

        for i in range(0, 7): # first few lines are bs
            self.gps_serial.readline()

        while self.running:
            data = str(self.gps_serial.readline()).replace("'", "").replace("b", "").split(",")
            command = data.pop(0)

            if command == "$GPGGA":
                self.parse_GGA(data)
            elif command == "$GPGLL":
                self.parse_GGL(data)
                print("GGL")
            elif command == "$GPRMC":
                self.parse_RMC(data)
                print("RMC")
            elif command == "$GPTRF":
                self.parse_TRF(data)
            elif command == "$GPVBW":
                self.parse_VBW(data)
            elif command == "$GPVTG":
                self.parse_VTG(data)
            else:
                pass
                # un-necessary command sentence

        self.gps_serial.close()

    def do_sample_rate(self):
        self.current_time = time.perf_counter()
        self.sample_rate = self.current_time - self.prev_time
        self.prev_time = self.current_time

    def stop_thread(self):
        self.running = False

    # --- Calculation functions ---

    def harversin(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Returns the distance between 2 points in KM

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        delta_lat = lat1 - lat2
        delta_lon = lon1 - lon2

        a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)
        c = 2 * asin(sqrt(a))
        return c * GPS_Interface.RADIUS_OF_EARTH

    def convert_min_to_decimal(self, position: str) -> float:
        # Converts the position in time into degrees
        try:
            temp = position.split(".")
            before = list(temp[0])

            if before[0] == '0':
                before.remove('0')

            degrees = float(before[0] + before[1])
            minutes = float(before[2] + before[3] + "." + temp[1])
        except:
            degrees = 0
            minutes = 0

        return degrees + minutes / 60

    # --- Parsing functions ---
    # there is more information to parse, to-do later, these are the essentials

    def parse_GGA(self, data: list):
        self.latitude = self.convert_min_to_decimal(data[1]) * (1 if data[2] == 'N' else -1)
        self.longitude = self.convert_min_to_decimal(data[3]) * (1 if data[4] == 'E' else -1)
        self.altitude = float(data[8])
        self.do_sample_rate()

    def parse_GGL(self, data: list):
        self.latitude = self.convert_min_to_decimal(data[0]) * (1 if data[1] == 'N' else -1)
        self.longitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] == 'E' else -1)
        self.do_sample_rate()

    def parse_RMA(self, data: list):
        if data[0] == 'A':
            self.latitude = self.convert_min_to_decimal(data[1]) * (1 if data[2] == 'N' else -1)
            self.longitude = self.convert_min_to_decimal(data[3]) * (1 if data[4] == 'E' else -1)
            self.ground_speed = float(data[7]) * GPS_Interface.KNOTS_TO_KM
            self.do_sample_rate()

    def parse_RMC(self, data: list):
        self.latitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] == 'N' else -1)
        self.longitude = self.convert_min_to_decimal(data[4]) * (1 if data[5] == 'E' else -1)
        self.ground_speed = float(data[6]) * GPS_Interface.KNOTS_TO_KM
        self.do_sample_rate()

    def parse_TRF(self, data: list):
        self.latitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] == 'N' else -1)
        self.longitude = self.convert_min_to_decimal(data[4]) * (1 if data[5] == 'E' else -1)
        self.do_sample_rate()

    def parse_VBW(self, data: list):
        self.ground_speed = float(data[4]) * GPS_Interface.KNOTS_TO_KM

    def parse_VTG(self, data: list):  # this may not be necessary
        pass

    # --- Get Data functions ---
    def get_sample_rate(self) -> float:
        return self.sample_rate

    def get_ground_speed(self) -> float:
        return self.ground_speed

    def get_position(self) -> list:
        return [self.latitude, self.longitude]

    def get_latitude(self) -> float:
        return self.latitude

    def get_longitude(self) -> float:
        return self.longitude

    def zero_location(self):
        self.relative_latitude = self.latitude
        self.relative_longitude = self.longitude

    def get_relative_distance(self) -> float:
        return self.harversin(self.relative_latitude, self.relative_longitude, self.latitude, self.longitude)

    def get_relative_bearing(self) -> float:
        # Returns bearing relative to "True" north
        # convert to degrees as well

        lat, lon = map(radians, [self.relative_latitude - self.latitude, self.relative_longitude-self.longitude])
        return atan(lon / lat)

    def get_distance_to(self, goal: list) -> float:
        # Expects the goal in decimal
        # Returns the distance in KM

        return self.harversin(goal[0], goal[1], self.latitude, self.longitude)

    def do_exit(self):
        self.stop_thread()
        self.gps_serial.close()



