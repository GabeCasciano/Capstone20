from serial import Serial
from serial import tools
from threading import *
from math import radians, cos, sin, asin, atan, sqrt

class GPS(Thread):

    data_queue = []
    NMEA_VALID_COMMANDS = ["GPGLL", "GPRMC", "GPTRF", "GPVBW", "GPVTG"]
    KNOTS_TO_KM = 1.852
    RADIUS_OF_EARTH = 6371

    def __init__(self, loc: str, baud: int):
        self.gps_serial = Serial(loc, baud)
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.ground_speed = 0
        self.how_valid = 0
        self.sats_in_use = 0

        self.relative_latitude = 0
        self.relative_longitude = 0

        self.running = True

        if not self.gps_serial.isOpen():
            self.gps_serial.open()

        self.gps_worker = self.worker(self.gps_serial)

    # --- Parsing thread ---

    def run(self) -> None:
        while self.running:
            data = str.split(self.ser.readline().__str__(), ",")
            command = data.pop()

            if command is "GPGGA":
                self.parse_GGA(data)
            elif command is "GPGLL":
                self.parse_GGL(data)
            elif command is "GPRMC":
                self.parse_RMC(data)
            elif command is "GPTRF":
                self.parse_TRF(data)
            elif command is "GPVBW":
                self.parse_VBW(data)
            elif command is "GPVTG":
                self.parse_VTG(data)
            else:
                pass
                # un-necessary command sentence

    # --- Calculation functions ---

    def harversin(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        # Returns the distance between 2 points in KM

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        delta_lat = lat1 - lat2
        delta_lon = lon1 - lon2

        a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)
        c = 2 * asin(sqrt(a))
        return c * GPS.RADIUS_OF_EARTH

    def convert_min_to_decimal(self, position: str) -> float:
        # Converts the position in time into degrees

        temp = list(position)
        degree = int(str.join(temp[0], temp[1]))
        minutes = int(str.join(temp[2], temp[3]))
        seconds = int(str.join(temp[4], temp[5]))

        return degree + minutes/60 + seconds/3600

    # --- Parsing functions ---
    # there is more information to parse, to-do later, these are the essentials

    def parse_GGA(self, data: list):
        if data.__len__() > 8:
            self.latitude = self.convert_min_to_decimal(data[1]) * (1 if data[2] else -1)
            self.longitude = self.convert_min_to_decimal(data[3]) * (1 if data[4] else -1)
            self.altitude = float(data[8])

    def parse_GGL(self, data: list):
        if data.__len__() > 6:
            if data[6] is 'A':
                self.latitude = self.convert_min_to_decimal(data[0]) * (1 if data[1] else -1)
                self.longitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] else -1)

    def parse_RMA(self, data: list):
        if data.__len__() > 7:
            if data[0] is 'A':
                self.latitude = self.convert_min_to_decimal(data[1]) * (1 if data[2] else -1)
                self.longitude = self.convert_min_to_decimal(data[3]) * (1 if data[4] else -1)
                self.ground_speed = float(data[7]) * GPS.KNOTS_TO_KM

    def parse_RMC(self, data: list):
        if data.__len__() > 6:
            self.latitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] else -1)
            self.longitude = self.convert_min_to_decimal(data[4]) * (1 if data[5] else -1)
            self.ground_speed = float(data[6]) * GPS.KNOTS_TO_KM

    def parse_TRF(self, data: list):
        if data.__len__() > 5:
            self.latitude = self.convert_min_to_decimal(data[2]) * (1 if data[3] else -1)
            self.longitude = self.convert_min_to_decimal(data[4]) * (1 if data[5] else -1)

    def parse_VBW(self, data: list):
        if data.__len__() > 4:
            self.ground_speed = float(data[4]) * GPS.KNOTS_TO_KM

    def parse_VTG(self, data: list):  # this may not be necessary
        pass

    # --- Get Data functions ---

    def get_velocity(self) -> float:
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

        lat, lon = map(radians, [self.relative_latitude - self.latitude, self.relative_longitude-self.longitude])
        return atan(lon / lat)

    def get_distance_to(self, goal: list) -> float:
        # Expects the goal in decimal
        # Returns the distance in KM

        return self.harversin(goal[0], goal[1], self.latitude, self.longitude)




